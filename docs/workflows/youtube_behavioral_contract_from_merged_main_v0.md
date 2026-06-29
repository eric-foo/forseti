# YouTube Behavioral Contract From Merged Main v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow record
scope: Source-backed extraction of the merged YouTube behavioral projection contract observed on origin/main at 6517dd10.
use_when:
  - Comparing Instagram/Reels capture behavior against the merged YouTube projection behavior before designing a shared capture core.
  - Recovering the YouTube-side field, status, source-key, residual, and boundary semantics without rereading the full implementation first.
authority_boundary: retrieval_only
```

## Scope

This record extracts the YouTube behavioral projection contract as observed on `origin/main` at `6517dd10`. It is not a shared-core architecture decision, not an Instagram/TikTok contract, not a live-capture validation report, and not a mandate that other lanes copy YouTube's acquisition method, priority order, packet shape, or transcript route.

Load-bearing sources read for this extraction:

- `orca-harness/youtube_capture/behavioral_projection.py`
- `orca-harness/tests/unit/test_youtube_behavioral_projection.py`
- `orca-harness/tests/contract/test_youtube_behavioral_projection_no_runtime_imports.py`
- `orca-harness/data_lake/root.py`

## Top-Level Projection

The projection module declares:

- `YOUTUBE_BEHAVIORAL_PROJECTION_METHOD = "youtube_behavioral_projection"`
- `YOUTUBE_BEHAVIORAL_PROJECTION_VERSION = "v0"`
- output `platform = "youtube"`
- output `platform_video_id`

`project_youtube_behavioral_item(...)` returns:

- `projection_method`
- `projection_version`
- `platform`
- `platform_video_id`
- `metadata_capture`
- `transcript`
- `behavioral_completeness`

`behavioral_completeness.status` is exactly the transcript extraction rollup status. `behavioral_completeness.complete` is true only when the rollup status is exactly `complete`. Residuals are accumulated in `behavioral_completeness.residuals`.

The projection requires a resolvable single video id. It uses the explicit `platform_video_id`, then the normalized metadata video id, then a single video id from transcript sources. It raises `ValueError` when no video id can be resolved, or when transcript sources span multiple video ids before an explicit or metadata video id is available.

## Metadata And Comments

`normalize_youtube_metadata_packet(...)` accepts legacy YouTube metadata/comment packet shapes and returns `None` if no packet is supplied or if no usable `platform_video_id` / `video_id` exists.

When present and video-matched, `metadata_capture` contains:

- `platform`
- `platform_video_id`
- `surface_type`
- `watch_url`
- `canonical_url`
- `channel`
- `metadata`
- `engagement`
- `comments`
- `receipts`

`comments` contains:

- `posture`, defaulting to `unknown`
- `comment_count_text`
- `sample_count`
- `sample`, bounded by `comment_sample_limit`

Metadata residuals:

- `youtube_metadata_packet_absent`
- `youtube_metadata_packet_video_mismatch:<metadata_video_id>`

A mismatched metadata packet is not projected as `metadata_capture`; it is residualized and dropped.

## Transcript Source Discovery

`transcript_sources_for_video(data_root, platform_video_id, rebuild_availability=False)` discovers committed local-lake YouTube transcript sources. It does not do live acquisition.

Discovery behavior:

- If `rebuild_availability=True`, it calls `data_root.rebuild_availability()`.
- Otherwise it reads the existing availability index through `data_root.list_available(source_family="youtube")`.
- For each packet id, it calls `data_root.load_raw_packet(packet_id)`.
- If `load_raw_packet` raises `DataLakeRootError`, discovery appends a fail-visible discovery source and continues.
- Loaded packets with `source_surface = "youtube_captions"` are projected as caption sources.
- Loaded packets with `source_surface = "youtube_audio"` are projected through the derived ASR records lane.
- Packets whose capture metadata video id does not match the requested video are skipped.

`rebuild_availability` is opt-in because rebuilding the index is a write. The unit tests pin that a stale/missing availability index returns no sources by default and only finds raw-derived sources when `rebuild_availability=True`.

`DataLakeRoot.load_raw_packet(...)` re-reads the raw manifest and preserved file bytes, checks size and SHA-256, and fails closed on missing, malformed, unreadable, escaping, or mismatched packet contents. The YouTube projection catches those failures at transcript discovery and turns them into source-level `discovery_failed` residuals instead of aborting healthy sources for the requested video.

## Transcript Source Shape

Every transcript source produced through `_base_transcript_source(...)` carries:

- `platform`
- `platform_video_id`
- `transcript_anchor`
- `transcript_source_key`
- `source_kind`
- `source_route`
- `source_status`
- `posture`
- `cue_count`
- `extraction_eligible`
- `non_eligible_reason`
- `capture_timestamp`

Caption sources add:

- `caption_kind`
- `language`
- `original_language_assumed`
- `title`
- `channel_id`

ASR sources add:

- `asr_record_id`
- `provenance`

Discovery-failure sources use:

- `source_kind = "discovery"`
- `source_route = "youtube_packet_discovery"`
- `source_status = "discovery_failed"`
- `posture = "discovery_failed"`
- `cue_count = 0`
- `capture_timestamp = None`
- `discovery_error`

Caption sources use `source_route = "youtube_captions"` and `source_kind = "caption"`. A caption source is `source_status = "complete"`; its posture is `caption_ready` when cue count is positive and `caption_empty` otherwise.

Audio packet sources route through derived ASR records with `source_route = "youtube_audio_asr"` and `source_kind = "asr"`. If no derived ASR records exist for an audio packet, the source is emitted as `source_status = "missing_derived_record"` and `posture = "missing_derived_record"`. If ASR record-set completion is absent, ASR record status is `partial_needs_cleanup`; otherwise it is `complete`.

## Eligibility

`extraction_eligible` is true only when all three are true:

- `source_status == "complete"`
- `cue_count > 0`
- `posture in {"caption_ready", "transcribed"}`

If a source is not eligible, `non_eligible_reason` is selected in this order:

- the non-complete `source_status`
- problem posture, currently `failed`
- `zero_cues`
- the posture value

When extraction status is attached, non-eligible sources receive `extraction_status = "not_extraction_eligible"`.

## Source Keys And Result Matching

`_source_key(...)` preserves an existing `transcript_source_key` when one is present. Otherwise it computes one with `_transcript_source_key(...)`:

- ASR: `<transcript_anchor>:asr:<asr_record_id-or-unknown_record>`
- Non-ASR: `<transcript_anchor>:<source_kind>`

Extraction results match in this order:

- exact key from `transcript_source_key`
- exact key from `source_key`
- synthesized exact key from `anchor` / `packet_id` plus `source_kind` and/or `asr_record_id`
- anchor-level fallback from `anchor` or `packet_id`

Anchor-level fallback is rejected as `ambiguous_anchor_result` when the anchor has duplicate eligible sources. Multiple anchor-level results for one source are also rejected as `ambiguous_anchor_result`.

When an eligible source has a matching extraction result, the source receives `extraction_status`. Matching results may also enrich the source with `extraction_record_path` from a result `path` and `extraction_error` from a result `error`.

## Extraction Statuses And Rollup

Complete extraction statuses:

- `extracted`
- `skipped_done`

Problem extraction statuses:

- `failed`
- `partial_needs_cleanup`
- `discovery_failed`
- `ambiguous_anchor_result`

Source completion problems:

- `partial_needs_cleanup`
- `missing_derived_record`
- `discovery_failed`

Source posture problems:

- `failed`

Rollup counts:

- `eligible_source_count`
- `complete_source_count`
- `incomplete_source_count`
- `source_problem_count`
- `extraction_problem_count`

Rollup status selection order:

1. `no_extraction_eligible_sources`, when there are no eligible sources.
2. `complete`, when all eligible sources are complete and there are no source problems.
3. `complete_with_residuals`, when all eligible sources are complete but source problems exist.
4. `partial_failed`, when at least one eligible source is complete and at least one eligible source has a problem extraction status.
5. `partial`, when at least one eligible source is complete and at least one eligible source is incomplete.
6. `failed`, when extraction problems exist and no eligible source is complete.
7. `source_problem`, when source problems exist and no earlier status matched.
8. `not_attempted`, otherwise.

Observed unit-test anchors:

- healthy metadata, comments, caption source, ASR source, and extracted results roll up to `complete`;
- corrupt or unreadable raw packet discovery does not abort a healthy caption source and rolls up to `complete_with_residuals` when the healthy source is extracted;
- observed but unextracted ASR keeps the video from being complete and rolls up to `partial`;
- duplicate eligible ASR sources with an anchor-only extraction result roll up to `failed` through `ambiguous_anchor_result`;
- failed ASR posture is counted as a source problem and can produce `complete_with_residuals` when the healthy caption source is extracted;
- failed extraction remains visible even when another source is merely not attempted;
- metadata-only comment posture is preserved but transcript completion is not claimed.

## Residual Vocabulary

Projection residuals are deduplicated and currently include these exact forms:

- `youtube_metadata_packet_absent`
- `youtube_metadata_packet_video_mismatch:<metadata_video_id>`
- `youtube_transcript_source_video_mismatch:<source_video_id>`
- `youtube_transcript_source_<source_status>:<source_key>`
- `youtube_transcript_source_<posture>:<source_key>`
- `youtube_transcript_source_not_extraction_eligible:<source_key>`
- `youtube_transcript_extraction_<extraction_status>:<source_key>`

The source-status residual form currently applies to `partial_needs_cleanup`, `missing_derived_record`, and `discovery_failed`. The posture residual form currently applies to `failed`. The extraction residual form currently applies to `failed`, `partial_needs_cleanup`, `discovery_failed`, and `ambiguous_anchor_result`.

## Canonical Transcript Source

`canonical_source` is selected only from eligible sources. If no eligible sources exist, it is `None`.

Ranking prefers:

1. manual captions;
2. other caption sources;
3. ASR sources.

Within the best rank, the selected source is the max by `capture_timestamp` and then `transcript_anchor`. The canonical shape contains:

- `transcript_anchor`
- `source_kind`
- `source_route`
- `caption_kind`
- `extraction_status`

## Acquisition Boundary

`orca-harness/youtube_capture/behavioral_projection.py` is a projection layer over already-captured inputs. The contract test forbids runtime acquisition and LLM import roots in that module:

- `aiohttp`
- `anthropic`
- `bs4`
- `httpx`
- `langchain`
- `litellm`
- `openai`
- `playwright`
- `requests`
- `scrapy`
- `selenium`
- `socket`
- `urllib.request`
- `urllib.error`

This boundary is important for the shared-core discussion: the useful commonality is the behavior/completeness projection and residual vocabulary, not a requirement that Instagram, YouTube, and TikTok share capture acquisition machinery.

## Transfer Notes For IG Sync

Use this as a YouTube reference contract for comparison, not as an implementation recipe for Instagram.

Important residuals to preserve as explicit design pressure:

- Discovery failures are target-video-projected even when the unreadable packet cannot prove its own video id. This keeps failures visible, but a future shared core may need a lane/global discovery residual channel to avoid pretending such failures are definitely target-specific.
- Availability-index discovery is read-only by default and can under-report when stale. Callers that need raw-derived discovery must opt into `rebuild_availability=True`.
- YouTube's strongest behavior is transcript/extraction completeness projection. Its weaker area remains acquisition coverage. Instagram should be compared against the behavioral completeness contract before any attempt to reuse machinery.
- The shared core should separate behavior projection concepts from lane-specific acquisition, packet discovery, and transcript-source discovery.
