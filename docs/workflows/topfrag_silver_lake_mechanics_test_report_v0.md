# TopFrag Silver-Lake Mechanics Test Report v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti workflow validation report
scope: Scratch-only TikTok Silver producer, lineage, selection, and recovery-admission mechanics over the pinned TopFrag eight-video staging set.
use_when:
  - Checking what the TopFrag scratch Silver run actually exercised and observed.
  - Reproducing or reviewing the bounded recovery-admission correction.
authority_boundary: retrieval_only
input_hashes:
  - tiktok_grid_window.json: 4804CEAC143F83DD9AC61A22B59D4F2027A84118DEB5618181DD2A4ABC43E97C
  - tiktok_grid_video_selection.json: 7986567F5C863923EA874B26486D95A48739C619B4E05BBC500991E720A816F1
  - transcript_backfill_v4/tiktok_live_cadence_result.json: E5A5895D4924CF8E74222F8CC0C0E261291D325B8E43FED3EFBEA90307ED0295
  - partial_v3/tiktok_live_cadence_result.json: 7751E9F4916B88FF4F5E1834BFA93F9A74C5A707636000BC17B650D20C50D680
  - recovery_v2/tiktok_live_cadence_result.json: 7673DA9253B8ED744548E291B596BE6B17AE01BAFF4F7B55B46729CD52BFEF08
branch_or_commit: codex/topfrag-silver-lake-mechanics-fix; original packet d486d94206110203e42aaa9683822b46d00081f8 rebased as 63dade2f onto cb5fc3f4
stale_if:
  - Any pinned input hash changes.
  - The TikTok batch admission, metric seed, Silver producer, snapshot selector, or reader contract changes.
```

```yaml
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: implementation-authorized
  target_scope: bounded recovery-admission correction plus scratch-only TopFrag Silver mechanics execution
  dirty_state_checked: yes
  blocked_if_missing: packet, pinned inputs, Silver contract, producer, reader, lineage front door, or scratch-root isolation
```

## Outcome

The scratch mechanics test passed over the exact eight selected TopFrag video ids. The run wrote only to `C:\tmp\topfrag-silver-mechanics-d486d942`; it did not write the live data lake, mutate Creator Registry, recapture TikTok, or create Gold/Judgment output.

One bounded defect blocked the first attempt: the multi-receipt batch-admission gate rejected the recovery receipt because it retained a failed video-6 attempt even though a later receipt completed that same video. The correction now permits only a strictly later `status=completed` row for the same video to supersede a failure and persists a sanitized supersession receipt. Missing, same-time, or older completions still fail closed.

## Input Resolution

- The five handoff-pinned file hashes matched exactly.
- The completed cadence rows were 5 from v4, 1 from v3, and 2 from v2. Their eight video ids exactly matched the selection receipt's eight ids.
- The v2 failure for `7658988386560036113` was observed at `2026-07-11T20:32:13Z`; the v2 run completed at `20:33:05Z`; the v3 completed recovery finished at `20:38:21Z`.
- The existing admission seam also requires a live-grid schema carrier. The adjacent v1 `tiktok_live_grid_result.json` was used without treating it as a newly pinned authority input. Its observed SHA256 was `14F25DC2481AC922162BCE808ADD9983501A01F832642EEE8BED44F416C42D7D`; all five rows it supplied matched the pinned 32-item window on video id, `playCount`, and `diggCount`. The remaining rows used their cadence `grid_candidate` fallback, as the existing seam specifies.

## Observed Mechanics

| Check | Observed result |
| --- | --- |
| Raw admission | One packet: `01KX9G3X0X8HB5JRN20JQJ0SE2` |
| Admitted videos | 8, in pinned review-priority order |
| First Silver cycle | 40 `MetricObservation` records + 1 `MetricRollupObservation` |
| Second append-only cycle | 40 observations + 1 rollup |
| Final scratch lake | 80 observations + 2 rollup siblings |
| Metric coverage | 5 named metrics for each of all 8 video subjects |
| Raw-anchor lineage | All 80 observation refs resolved to the one preserved batch body and reproduced its SHA256 `d9266ca9e25fac6ebd18383e8611769beeaf6f987eb4533ead90e39a343772f9` |
| Derived lineage | All 48 rollup `derived_refs` resolved by record id and content hash |
| Durable integrity | All 82 Silver record content hashes reproduced independently from canonical JSON excluding `content_hash` |
| Subject identity | Native TikTok video ids and public handle `topfrag.official` were stable across records; the platform-account ref was the explicit scratch token `scratch_tt_topfrag_official` |
| Policy fingerprints | Metric registry `creator_metric_tiktok_batch_admission_v0`; rollup recipe `creator_metric_rollup_tiktok_profile_grid_engagement_v0`; producer schema versions and canonical content-hash basis present |
| Idempotent read selection | Re-running snapshot selection with no new record selected the same record id/hash and wrote no Silver record |
| Supersession selection | A later append-only cycle retained the first rollup and selected the new sibling at `selection_run_id=2` |
| Reader | Read both rollup siblings from the raw anchor; snapshot selection chose `01KX9G96BKXY53A4WX4ZYX96M1.json` over `01KX9G3XNST9B5297D3WKSN7XP.json` |

The producer is append-only, not write-idempotent: invoking it again intentionally creates new siblings. The idempotency verified here is the read/snapshot behavior when no new record exists. Supersession is explicit in selection-manifest state and reader choice; this TikTok metric lane does not emit a separate `supersedes_record` relationship record.

## Patch And Validation

Changed:

- `forseti-harness/source_capture/tiktok/batch_packet.py`
- `forseti-harness/tests/unit/test_tiktok_batch_admission.py`

Red/green proof:

- Before the correction, both new focused tests failed at the unconditional `contains 1 failure entries` rejection.
- After the correction, the later-completion case passed and the older-completion case remained a fail-closed rejection.
- Focused suite: `52 passed` across TikTok admission, TikTok Silver producer, TikTok rollup runner, creator-metric Silver reader, and the Silver reader selection contract gate.
- Real scratch audit: exit 0 with all record counts, source hashes, content hashes, lineage refs, idempotent selection, sibling supersession, and reader selection assertions enabled.
- Full harness attempt: the command timed out after 120.8 seconds at 6% progress. No failure had appeared in the emitted portion, but this is not a full-suite pass claim.

## Advisory: Image And Sticker Comments

The pinned TopFrag cadence receipts preserve 142 parsed comments across eight successful comment-list bodies. Exactly one comment text contains a sticker marker: `[Sticker] bro literally like this`. Every preserved comment has the same field shape: `cid`, `text`, `create_time`, `digg_count`, `reply_comment_total`, and `user`. Neither the live-probe normalizer nor the batch-admission normalizer preserves comment media fields, and the field-coverage receipt has no media axis.

This is enough for Silver to state only that the captured text included a `[Sticker]` marker. It is not enough to prove that an image/sticker asset existed, distinguish a platform sticker from user text, resolve or hash an asset, determine dimensions or MIME type, render it, run OCR/vision, or represent its visual meaning. The eight response-body receipts carry hashes and byte counts (930,291 bytes total; 103,470–135,788 bytes each), but the raw response bodies were deliberately not persisted, so those hashes cannot recover the dropped media structure.

No separate pinned noeldeyzel comment artifact was present in the handoff or repository-visible capture set; repository hits were Creator Registry identity rows only. Therefore this advisory makes strict claims about the pinned TopFrag artifacts and the shared TikTok parser shape, not about a noeldeyzel capture.

### Ownership Boundary

- **Capture/Bronze owns** observing the source-native media fields, sanitizing them, preserving a source-native asset id when present, hashing any transient URL instead of persisting signed URLs, recording MIME/dimensions/declared size when source-visible, and optionally admitting fetched bytes as a hash-addressed Attachment Record under separate authorization.
- **Silver owns** a mechanical, lineage-closed statement that a particular comment contains a media reference, plus a pointer to the Capture/Bronze record or Attachment Record. Silver must not copy transient URLs as authority, fabricate an asset from `[Sticker]` text, or describe what the image means.
- **Cleaning/derived processing may own** deterministic OCR or normalization with model/policy fingerprints and derived refs. Semantic interpretation, relevance, sentiment, identity inference, or action meaning remains Judgment/Gold.

### Smallest Viable Future Seam

The smallest future seam is metadata-first and Capture-owned: extend the sanitized comment item with a sparse `media_refs` list carrying `kind`, source-native asset id when available, URL SHA256, dimensions/MIME/declared size when source-visible, capture posture, and a JSON-pointer anchor to the hashed comment-list body. Do not download media in that seam. A later Silver producer can emit a source-backed media-presence observation or comment relationship that points to this metadata; actual bytes and vision remain separately authorized follow-ons.

Estimated incremental burden, stated as scenarios rather than observed asset sizes:

| Future posture | Incremental storage | Token / vision burden |
| --- | --- | --- |
| Sparse metadata only | About 0.2–0.5 KB per media-bearing comment; under 1 KB for the one observed marker; roughly 28–71 KB if all 142 comments carried one ref | Roughly 50–150 serialized text tokens per media-bearing comment; no vision call |
| External/hash reference, no bytes | Same metadata range; zero image-binary storage in Silver | One optional future vision input per unique asset; text context remains metadata-sized |
| Persisted attachment later | `asset_count × average_asset_bytes`; illustrative 50 KB / 250 KB / 1 MB assets would make 142 assets about 7.1 / 35.5 / 142 MB | Vision cost scales with unique asset count and resolution; deduplicate by asset hash and never inline base64 into prompts |

The current pinned set has only one marker, so metadata-only support would be negligible. The expensive step is not Silver representation; it is separately authorized asset retrieval and vision processing.

## Residuals And Non-Claims

- `scratch_tt_topfrag_official` is an explicit test token, not Creator Registry truth or a claim that an authoritative platform-account id exists.
- The v1 live-grid schema carrier is hash-recorded and cross-checked but was not one of the handoff's five pinned files.
- The producer's accepted missing-Bronze-Attachment-Record residual remains; raw refs use the verified packet body.
- No separate Silver `supersedes_record` relationship edge was produced; only the existing manifest/reader supersession mechanism was tested.
- Not live-lake readiness, Creator Registry readiness, full Silver/Vault validation, buyer proof, Gold/Judgment validity, or permission for a future live write.
