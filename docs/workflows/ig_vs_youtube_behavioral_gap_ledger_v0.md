# IG vs YouTube Behavioral Gap Ledger v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow record
scope: Source-backed Instagram/Reels gap ledger against the PR #432 YouTube behavioral contract reference.
use_when:
  - Deciding the next IG behavior-sync patch after the YouTube behavioral contract adjudication lane.
  - Checking which IG behavior should match the YouTube completeness contract without copying YouTube acquisition mechanics.
  - Recovering accepted IG residuals before a future implementation-scoping or review pass.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/ig_behavioral_sync_from_youtube_contract_handoff_v0.md
  - docs/workflows/youtube_behavioral_contract_from_merged_main_v0.md
  - docs/workflows/shared_capture_core_ig_youtube_tiktok_planning_v0.md
  - docs/workflows/ig_backfix_against_youtube_behavioral_contract_spec_v0.md
  - orca-harness/source_capture/ig_reels_grid_projection.py
  - orca-harness/source_capture/transcript/ig_reels_audio_packet.py
  - orca-harness/source_capture/ig_reels_deep_capture.py
  - orca-harness/source_capture/ig_reels_deep_capture_lake.py
  - orca-harness/runners/run_ig_reels_product_extract.py
branch_or_commit: codex/ig-behavioral-sync-gap-ledger @ 5afa4660, branched from PR #432 head
stale_if:
  - PR #432 closes without merge or is superseded by a different YouTube behavioral contract.
  - Any named IG grid, deep-capture, audio transcript, persistence, extraction, or focused test source changes.
  - The owner authorizes implementation and a later implementation-scoping record supersedes this ledger.
```

## Status

Patch decision: `DOCS_PATCH_ONLY`.

This ledger completes the source refresh requested by
`docs/workflows/ig_behavioral_sync_from_youtube_contract_handoff_v0.md`. It does
not authorize IG runtime edits, live capture, shared-core implementation, or
YouTube acquisition-shape copying.

Implementation remains blocked until the owner explicitly authorizes bounded
source-changing IG parity work. If that happens, run the assumption gate and
fused implementation path against this ledger and the fresh source files before
editing.

## Start Preflight

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom handoff load contract plus IG/YT focused implementation and tests
  edit_permission: docs-write
  target_scope: IG behavior-sync gap ledger and bounded patch decision
  dirty_state_checked: yes
  blocked_if_missing: PR #432 live state, YouTube behavioral contract, IG source/test reread, capture playbook/recon reread
```

Cynefin route: complicated with one complex dependency. PR #432 is open draft,
so the YouTube contract is a PR-branch reference, not merged-main authority. The
safe decomposition is source refresh -> gap ledger -> patch decision.

## Confirmed Reference State

Live PR check observed by `gh pr view 432 --json state,isDraft,baseRefName,headRefName,headRefOid,mergedAt,url`:

- PR #432: `OPEN`, draft, base `main`, head `codex/youtube-contract-review-adjudication`.
- Head OID: `5afa46609549d384235ffc9072680f44919e933b`.
- `mergedAt`: `null`.

Implication: use the PR #432 branch/head as the YouTube behavioral reference for
this ledger. Do not claim the YouTube contract is merged into `origin/main`.

## Source Read Ledger

Project and workflow controls:

- `AGENTS.md`: Orca operating rules, docs-write default, implementation authorization boundary, and worktree isolation rule.
- `.agents/workflow-overlay/README.md`: overlay binding source.
- `.agents/workflow-overlay/source-loading.md`: confirm-don't-trust source loading, start preflight, capture playbook auto-load.
- `.agents/workflow-overlay/decision-routing.md`: Cynefin trigger and router shape.
- `.agents/workflow-overlay/retrieval-metadata.md`: retrieval header contract for this durable workflow record.
- `.agents/workflow-overlay/artifact-folders.md`: `docs/workflows/` accepted location.

Capture method references:

- `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`: capture playbook; non-authorizing, public-content/access-control/rate posture, no live capture authority.
- `orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md`: recon index; IG and YouTube social-source substrate context, not direct validation.

Behavior reference docs:

- `docs/workflows/ig_behavioral_sync_from_youtube_contract_handoff_v0.md`: active objective and drift guard.
- `docs/workflows/youtube_behavioral_contract_from_merged_main_v0.md`: YouTube behavioral contract reference.
- `docs/workflows/shared_capture_core_ig_youtube_tiktok_planning_v0.md`: thin-core planning and no-framework drift guard.
- `docs/workflows/ig_backfix_against_youtube_behavioral_contract_spec_v0.md`: prior IG back-fix planning spec.

IG implementation and tests:

- `orca-harness/source_capture/ig_reels_grid_projection.py`
- `orca-harness/source_capture/transcript/ig_reels_audio_packet.py`
- `orca-harness/source_capture/ig_reels_deep_capture.py`
- `orca-harness/source_capture/ig_reels_deep_capture_lake.py`
- `orca-harness/source_capture/ig_projection.py`
- `orca-harness/runners/run_source_capture_ig_reels_grid_packet.py`
- `orca-harness/runners/run_source_capture_ig_reels_audio_packet.py`
- `orca-harness/source_capture/ig_reels_comments.py`
- `orca-harness/runners/run_source_capture_ig_reels_deep_capture.py`
- `orca-harness/runners/run_ig_reels_product_extract.py`
- Focused tests:
  `test_source_capture_ig_reels_projection.py`,
  `test_ig_reels_audio_packet.py`,
  `test_ig_reels_deep_capture.py`,
  `test_ig_reels_deep_capture_lake.py`,
  `test_ig_reels_product_extract.py`.

## YouTube Reference Behavior

Use the YouTube contract as a behavior reference, not an implementation recipe.

The reference behavior to compare is:

- one projected item keyed by a resolvable single YouTube video id;
- metadata/comments posture preserved when present;
- transcript sources carry route, source status, posture, cue count, eligibility, and source keys;
- extraction statuses are attached to transcript sources;
- per-item `behavioral_completeness.status` is the extraction rollup, and `complete` is true only when the rollup is exactly `complete`;
- runtime acquisition and LLM imports stay outside the projection module;
- residuals keep discovery, source, posture, metadata mismatch, and extraction problems visible.

## Gap Ledger

| Area | Current IG source-backed behavior | YouTube-level behavior to match | Gap / decision |
| --- | --- | --- | --- |
| Identity | Grid projection rows carry `entity_namespace="instagram"` and `content_shortcode`; audio transcript records carry both `video_id` and `shortcode` as the IG shortcode; deep-capture record sets are anchored by shortcode. Sources: `ig_reels_grid_projection.py:109-137`, `ig_reels_audio_packet.py:193-207`, `ig_reels_audio_packet.py:293-307`, `ig_reels_deep_capture_lake.py:142-148`. | A single item key must resolve before projecting a completeness claim. | Match behavior by naming `platform_item_id=shortcode`. Do not rename every physical anchor first. Gap remains: no single IG behavioral record or index ties grid packet id, audio packet id, deep-capture record id, transcript anchor, comments, and extraction anchor together. |
| Candidate/ranking limits | Grid capture is logged-out `/reels/` page-load only, no item fanout; it preserves DOM rows, passive JSON candidates, joined rows, pinned inference, warning notes, limitation notes, and receipt non-claims. Static `/p/` rows are filtered from the reels traction series and static view count is not applicable. Sources: `run_source_capture_ig_reels_grid_packet.py:141-177`, `run_source_capture_ig_reels_grid_packet.py:262-330`, `ig_reels_grid_projection.py:421-459`. | Candidate/ranking evidence should stay visible without overclaiming traction strength. | Mostly matches. Required future patch is vocabulary/record shape, not acquisition. The behavior record should expose ranking basis and metric limitations as first-class fields rather than leaving them only in packet slices and projection rows. |
| Source-surface disagreement | Grid projection re-attaches all source-surface count candidates, marks missing JSON, rejects ambiguous duplicate-shortcode anchors, and never reports DOM as the chosen source surface. Sources: `ig_reels_grid_projection.py:95-137`, `ig_reels_grid_projection.py:498-519`, `ig_reels_grid_projection.py:622-640`; tests at `test_source_capture_ig_reels_projection.py:39-69`, `test_source_capture_ig_reels_projection.py:226-257`, `test_source_capture_ig_reels_projection.py:292-342`. | Source disagreements and ambiguous anchors should become residuals or limitations, not hidden assumptions. | Matches the behavioral direction. Future behavior record should carry this as per-item residual/limitation pressure. |
| Comments posture | Deep capture parses `AudienceComment` records from rendered DOM, dedupes by comment id, skips incomplete nodes, and returns comments when render succeeds even if audio fails. Sources: `ig_reels_comments.py:113-167`, `ig_reels_deep_capture.py:190-226`; tests at `test_ig_reels_deep_capture.py:178-209`. | Comment posture should distinguish captured, empty, blocked/render unavailable, parse failed, and not attempted. | Gap remains. Current source carries comments and failure notes, but not a normalized `IGCommentSet` posture. `render_unavailable` is represented through transcript posture/no comments, not a dedicated comment posture. |
| Transcript source records | Standalone audio writes a raw `SourceCapturePacket` with `source_family="instagram_creator"` and `source_surface="ig_reels_audio"`, then appends a `transcript_asr` derived record with posture, cues, provenance, source packet id, file id, and SHA. Sources: `ig_reels_audio_packet.py:222-261`, `ig_reels_audio_packet.py:293-318`; tests at `test_ig_reels_audio_packet.py:69-104`, `test_ig_reels_audio_packet.py:170-236`. | Transcript sources should carry route, source status, posture, cue count, eligibility, and source key. | Partial match. Standalone audio has enough raw material for a normalized transcript-source record, but the normalized record does not exist yet. |
| Deep-capture transcript source | One render yields both comments and media handle; runner statuses include `render_unavailable`, `no_audio_handle`, and `download_failed`; persisted deep-capture record sets contain transcript posture, cues, media provenance, and completion marker. Sources: `ig_reels_deep_capture.py:171-226`, `ig_reels_deep_capture_lake.py:101-148`; tests at `test_ig_reels_deep_capture.py:136-209`, `test_ig_reels_deep_capture_lake.py:43-69`, `test_ig_reels_deep_capture_lake.py:107-132`. | All observed transcript sources should either enter the transcript-source set or be explicit non-canonical residuals with deterministic lookup. | Gap remains and is sharper than the old spec: the deep-capture runner can carry `ok` as transcriber posture while standalone audio normalizes to `transcribed/no_speech/failed`. A future patch must normalize deep-capture posture before using it in a shared completeness rollup. |
| Transient media handling | Deep-capture media URLs are transient handles and are redacted from persisted payloads; only provenance such as host and handle-used status persists. Sources: `ig_reels_deep_capture.py:135-139`, `ig_reels_deep_capture_lake.py:113-132`; tests at `test_ig_reels_deep_capture_lake.py:60-69`. | Persistence can differ by platform if non-durable/transient artifacts are not laundered into evidence. | Matches. Keep IG-specific redaction and do not copy YouTube packet anchors or caption artifacts into IG. |
| Run receipts | Grid packets carry packet receipt metadata, limitations, warnings, visible mode changes, non-claims, and access/media/archive postures. Audio runner has typed exit statuses for access-gated, unavailable, and ASR failure visibility. Deep-capture runner prints per-run comments/transcript/audio-handle posture and optionally persists a record set. Sources: `run_source_capture_ig_reels_grid_packet.py:183-217`, `run_source_capture_ig_reels_grid_packet.py:297-334`, `run_source_capture_ig_reels_audio_packet.py:55-77`, `run_source_capture_ig_reels_deep_capture.py:218-247`. | Completeness should be inspectable from durable records, not stdout or human convention. | Gap remains. Grid/audio have stronger receipt surfaces than deep capture. Deep-capture stdout is not enough for a behavior-level run receipt; persisted record-set completion is not a complete run receipt. |
| Persistence correlation | Grid projection reads raw packet bytes and projects rows; audio transcript is a derived record under the audio packet id; deep capture is a shortcode-anchored derived record set; product mentions are under transcript anchors. Sources: `ig_reels_grid_projection.py:198-316`, `ig_reels_audio_packet.py:310-318`, `ig_reels_deep_capture_lake.py:142-148`, `run_ig_reels_product_extract.py:164-203`. | A future reader should resolve item -> transcript/comment/extraction anchors programmatically. | Gap remains. Current surfaces are deterministic individually, but there is no single shortcode-to-all-anchors bridge/index. Do not pretend packet id, shortcode, and record-set anchors are one physical shape. |
| Extraction feed | IG extraction discovers `instagram_creator` packets but only uses `source_surface="ig_reels_audio"`; it skips grid packets, reads `transcript_asr` derived records, uses only `transcribed` records with cues, and returns statuses `extracted`, `skipped_done`, `partial_needs_cleanup`, `failed`, and `discovery_failed`. Sources: `run_ig_reels_product_extract.py:112-136`, `run_ig_reels_product_extract.py:139-209`; tests at `test_ig_reels_product_extract.py:133-212`. | Source extraction statuses should feed a per-item rollup and avoid hidden complete claims. | Partial match. Status vocabulary exists at transcript-anchor level for standalone audio only. Deep-capture transcript records are currently outside this extraction feed. There is no per-item extraction rollup comparable to YouTube `behavioral_completeness`. |
| Residual visibility | Current IG residuals/failures include missing shortcode, missing JSON, ambiguous shortcode join, no passive JSON join, static view-count not applicable, access-gated audio, unavailable audio, transcriber failure posture, render unavailable, no audio handle, download failed, discovery failed, extraction failed, and partial cleanup. Sources above. | Residuals should be centralized enough that an item cannot claim complete while a source failed or was skipped silently. | Gap remains. Residuals are real but distributed across packet limitations, projection residuals, runner exit statuses, transcript posture, and extraction result rows. A behavior projection/index should centralize them before any per-item completeness claim. |
| Focused tests | Focused tests cover grid projection disagreement/static handling, audio identity/provenance/postures, deep-capture comments/audio-handle outcomes, deep-capture lake completion/redaction, and audio-only extraction statuses. | Tests should prove the behavior contract that future source-changing patches depend on. | Existing tests support current source facts. Missing tests: single IG behavioral record, comment posture normalization, transcript-source record normalization across standalone/deep capture, deterministic shortcode-to-anchor correlation, deep-capture extraction residualization, and per-item extraction rollup. |

## Accepted Residuals

- IG can remain ASR-only in v0.
- IG can keep separate grid, deep-capture, standalone-audio, and extraction runners.
- IG can keep shortcode-anchored deep-capture record sets and packet-id-anchored audio transcripts if a deterministic bridge/index is added before any whole-item completeness claim.
- Deep-capture transcript extraction can remain a named residual only if the behavior record makes it discoverable and prevents hidden `complete` claims.
- YouTube PR #432 can remain the planning reference while open, but it is not merged-main authority.

## Patch Decision

Decision: `DOCS_PATCH_ONLY`.

The older IG back-fix spec remains broadly aligned with current source reads,
but it should not authorize implementation by itself. This ledger is the fresh
source-backed patch decision:

1. No IG runtime patch in this lane without explicit bounded implementation authorization.
2. The next implementation target, if authorized, should be an IG behavioral projection/index over existing surfaces, not an acquisition rewrite.
3. The first implementation patch should make item-level behavior inspectable:
   shortcode identity, ranking limitations, comments posture, transcript-source records, run receipts, persistence anchors, extraction source statuses, per-item rollup, and residuals.
4. Do not copy YouTube's HTTP/youtubei route, caption priority, packet anchors, runner structure, or acquisition method into IG.

## Validation

Focused tests passed in the isolated worktree:

```text
$env:PYTHONDONTWRITEBYTECODE=1; python -m pytest -p no:cacheprovider -q --basetemp .pytest_tmp_ig_behavioral tests/unit/test_source_capture_ig_reels_projection.py tests/unit/test_ig_reels_audio_packet.py tests/unit/test_ig_reels_deep_capture.py tests/unit/test_ig_reels_deep_capture_lake.py tests/unit/test_ig_reels_product_extract.py
........................................................................ [ 97%]
..                                                                       [100%]
```

Earlier, the PR #432 reference worktree was read-only for practical test/write
purposes because creating its `_scratch` test directory hit a Windows ACL
`PermissionError`. This ledger was therefore written and verified in the
separate `codex/ig-behavioral-sync-gap-ledger` worktree.

## Non-Claims

This ledger does not claim:

- PR #432 is merged;
- IG parity is implemented;
- live IG capture was run;
- shared capture core implementation is authorized;
- YouTube acquisition coverage is complete;
- TikTok behavior is known;
- product readiness, legal/access approval, or live-scale validation.
