# YouTube Behavioral Measurement Corpus Receipt v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow receipt
scope: Canonical F-lake YouTube behavioral measurement corpus after expanding beyond the initial two-video proof.
use_when:
  - Checking whether YouTube behavioral evidence is statistically measurable.
  - Distinguishing caption-route source/caption coverage from full behavioral completion.
  - Recovering the current YouTube canonical F-lake corpus counts after the 2026-06-30 expansion run and leading-dash residual retry.
open_next:
  - docs/workflows/ig_youtube_behavioral_e2e_closeout_receipt_v0.md
  - docs/workflows/youtube_behavioral_contract_from_merged_main_v0.md
  - orca-harness/runners/run_source_capture_youtube_watch_packet.py
  - orca-harness/runners/run_source_capture_youtube_caption_packet.py
  - orca-harness/runners/run_source_capture_youtube_asr_packet.py
  - orca-harness/youtube_capture/behavioral_projection.py
stale_if:
  - YouTube packets, transcript packets, or product-mention records are added to or removed from F:/orca-data-lake.
  - The YouTube behavioral projection, transcript discovery, product-extraction, or source-lineage semantics change.
  - A later YouTube measurement receipt supersedes this corpus.
authority_boundary: retrieval_only
```

## Short Answer

The corpus is now large enough to measure the **YouTube caption-route behavioral projection
path** under the current operator/Codex extraction boundary.

It is still not large enough to statistically claim **platform-wide YouTube behavioral
completeness**, because ASR/no-caption fallback remains unmeasured and the product extraction
batch was not provider-API extraction.

Observed canonical `F:/orca-data-lake` state:

```text
YOUTUBE_PACKET_COUNT 64
YOUTUBE_VIDEO_COUNT 33
SURFACE_COMBOS
youtube_captions+youtube_watch_metadata_comments 31
youtube_watch_metadata_comments 2
PROJECTION_STATUS_COUNTS
complete 31
no_extraction_eligible_sources 2
YOUTUBE_PRODUCT_RECORDS 31
YOUTUBE_PRODUCT_MENTIONS_TOTAL 122
```

Interpretation:

- Caption-route source/caption coverage is measurable at `n=31`: every item in that cell has both
  `youtube_watch_metadata_comments` and `youtube_captions` packets.
- Caption-route behavioral projection completion is now measurable at `31/31` for that cell: every
  caption-ready video has a completed source-lineage-bearing Silver product-mention record.
- Whole observed YouTube-video completion is `31/33`; the remaining two videos are watch-only
  current-source failures with no extraction-eligible transcript source.
- ASR/no-caption fallback is not measurable: the attempted ASR seed wrote a watch packet, but audio
  download failed and the caption probe reported the video as removed/unavailable.
- The seed is a fragrance YouTube Shorts seed, not a random platform sample; do not generalize to all
  YouTube or all creator content.

## Corpus Build

The expansion used the existing YouTube Shorts fragrance seed as the candidate source and targeted
30 caption-route videos with both watch metadata/comments and caption transcript packets. A follow-up leading-dash residual retry added one more watch+caption video, bringing the current caption-route cell to 31.

Starting state before this pass:

```text
START_WATCH 2 ['VOGZUccarFc', 'ljZ7_JHXNdw']
START_CAPTION 2 ['VOGZUccarFc', 'ljZ7_JHXNdw']
START_COMPLETE 2 ['VOGZUccarFc', 'ljZ7_JHXNdw']
```

Batch result:

```text
FINAL_WATCH 31
FINAL_CAPTION 30
FINAL_COMPLETE 30
RESULT_COUNTS {"attempts": 30, "caption_failed": 2, "caption_ok": 28, "watch_failed": 1, "watch_ok": 29}
```

Additional ASR-route probe:

```text
as7hye0qgYc watch packet: wrote F:/orca-data-lake/raw/f69/01KWBPYB766MZ89C2D23VCS0DN
as7hye0qgYc ASR audio download: failed with "audio download failed"
as7hye0qgYc caption probe: failed with "Video unavailable. This video has been removed by the uploader"
```

Failed/residual candidates observed during corpus construction:

| Video id | Route expectation | Observed result | Interpretation |
| --- | --- | --- | --- |
| `-V7MN2IWMpA` | caption | fixed in follow-up: watch packet, caption packet, and Silver product-mention record now read back complete | Former batch invocation edge for leading-dash video ids; now included in the complete caption-route corpus. |
| `JcwT5rvhXIc` | caption | watch packet wrote; caption failed as removed by uploader | Current-source unavailability; contributes watch-only/no-transcript case, not caption-route success. |
| `as7hye0qgYc` | ASR | watch packet wrote; ASR audio download failed; caption probe says removed by uploader | ASR/no-caption stratum remains unmeasured and needs replacement candidates. |

## Leading-Dash Residual Retry

A follow-up residual-burndown patch normalized only the `--video-id <value>` argv pair when the value is a valid 11-character YouTube id that starts with `-`. The formerly failing command shape then reached live capture and wrote canonical F-lake packets for `-V7MN2IWMpA`.

Observed packet and Silver writes:

```text
WATCH_PACKET F:/orca-data-lake/raw/dca/01KWBVE0XV1E1MRY3KS538ZJE3
CAPTION_PACKET F:/orca-data-lake/raw/266/01KWBVEVSGVEE3VHY3F5RK4ZQ1
SILVER_RECORD F:/orca-data-lake/derived/266/01KWBVEVSGVEE3VHY3F5RK4ZQ1/silver__cleaning__product_mentions/mentions_codex_operator_youtube_residual_burndown_v0__8a95674a2ab08d69.json
MENTIONS 2
REJECTED 0
PROJECTION -V7MN2IWMpA status=complete sources=1 complete_sources=1 mentions=2 residuals=[]
```

First F-lake retry note: the initial watch retry got past argparse but failed during staging after writing only `raw/01_raw_watch.html` under `F:/orca-data-lake/.staging/01KWBVATV7KWQWK4FP2JDND4MD`. The immediate retry succeeded with the committed watch packet above; the partial staging directory was verified and removed.

Complete caption-route video ids:


```text
-V7MN2IWMpA, 17mhHUkRLvg, 1K9ej-6aP6g, 5QDcTenklxg, 5e4y5yNagRI, 6k8ebJw50tU, 7S40eU8FDCY, Fd-aChpt_Ss, FqTrOZbh_DE, JMmEIv_oG4o, Ln1LUflj8d0, MN3AI-mrPWk, Tb-_V-JVNfk, Uj4bVTM6dm8, VOGZUccarFc, WEqUWKA4FUI, WcSRnnwSAJM, XDscn2sgW3w, _Gp2AmN74E8, bPJCH9iQUhI, ekaQONEC2ys, hfyoVdOAYt4, jo03W7cBwBM, ljZ7_JHXNdw, rmDwkTrzNxo, sy-rczzFrYg, uaCSynFfPpc, vl-QUTwtneY, vtwo-iaOszA, xK8bmugSpgQ, xZ6vd9fyBbw
```

Watch-only video ids:

```text
JcwT5rvhXIc, as7hye0qgYc
```

## Product Extraction Boundary

No provider extraction was available during the corpus passes or leading-dash retry:

```text
OPENAI_API_KEY_SET False
ANTHROPIC_API_KEY_SET False
ORCA_PRODUCT_EXTRACT_PROVIDER <unset>
ORCA_PRODUCT_EXTRACT_MODEL <unset>
```

The first two YouTube product records were the earlier explicitly labeled operator records. The
follow-up batch then read the 28 remaining caption-ready transcripts and wrote them through the same
validated silver write boundary. The later leading-dash retry added one more operator-assisted record through that same boundary:

```text
DRY_PARSE
mapping_videos 28
transcripts_found 28
requested_mentions 108
accepted_mentions 108
rejected_mentions 0

WRITE_MODEL codex_operator_youtube_measurement_batch_v0
WRITE_BACKEND codex_operator_measurement_batch_current_thread
WRITTEN_COUNT 28
SKIPPED_COUNT 0
WRITTEN_MENTION_TOTAL 108
EMPTY_COMPLETE_WRITES 2
```

Fresh readback after the batch and leading-dash residual retry:

```text
YOUTUBE_PRODUCT_RECORDS_COMPLETE 31
YOUTUBE_PRODUCT_MENTIONS_TOTAL 122
YOUTUBE_PRODUCT_BACKENDS {"codex_operator_assisted": 1, "codex_operator_manual_current_thread": 2, "codex_operator_measurement_batch_current_thread": 28}
YOUTUBE_PRODUCT_LINEAGE_SURFACES {"youtube_captions": 31}
```

Two batch records are complete zero-mention records because the caption text did not carry a safe
named product:

| Video id | Anchor | Record id | Reason |
| --- | --- | --- | --- |
| `5e4y5yNagRI` | `01KWBPTGHVHW2AV19QQ14FKV1J` | `mentions_codex_operator_youtube_measurement_batch_v0__c8c9b67507a04c48.json` | garbled/current-source caption with no safe named product |
| `WcSRnnwSAJM` | `01KWBPTTPJKB6TN26NPN7WXX7A` | `mentions_codex_operator_youtube_measurement_batch_v0__0e8c77f4dddfc6f5.json` | product discussion captured as `this fragrance` with no product name |

This closes the previous `not_attempted` extraction-run gap for the caption-route corpus. It does not
turn the batch into live provider-API extraction.

## Projection Matrix

Fresh projection readback after the operator/Codex batch and leading-dash residual retry:

```text
PROJECTION_STATUS_COUNTS
complete 31
no_extraction_eligible_sources 2
```

| Video id | Surfaces | Status | Sources | Eligible | Complete sources | Caption cues | Extraction statuses |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| `-V7MN2IWMpA` | `youtube_captions+youtube_watch_metadata_comments` | `complete` | 1 | 1 | 1 | 191 | `extracted` |
| `17mhHUkRLvg` | `youtube_captions+youtube_watch_metadata_comments` | `complete` | 1 | 1 | 1 | 101 | `extracted` |
| `1K9ej-6aP6g` | `youtube_captions+youtube_watch_metadata_comments` | `complete` | 1 | 1 | 1 | 65 | `extracted` |
| `5QDcTenklxg` | `youtube_captions+youtube_watch_metadata_comments` | `complete` | 1 | 1 | 1 | 85 | `extracted` |
| `5e4y5yNagRI` | `youtube_captions+youtube_watch_metadata_comments` | `complete` | 1 | 1 | 1 | 13 | `extracted` |
| `6k8ebJw50tU` | `youtube_captions+youtube_watch_metadata_comments` | `complete` | 1 | 1 | 1 | 27 | `extracted` |
| `7S40eU8FDCY` | `youtube_captions+youtube_watch_metadata_comments` | `complete` | 1 | 1 | 1 | 43 | `extracted` |
| `Fd-aChpt_Ss` | `youtube_captions+youtube_watch_metadata_comments` | `complete` | 1 | 1 | 1 | 31 | `extracted` |
| `FqTrOZbh_DE` | `youtube_captions+youtube_watch_metadata_comments` | `complete` | 1 | 1 | 1 | 29 | `extracted` |
| `JMmEIv_oG4o` | `youtube_captions+youtube_watch_metadata_comments` | `complete` | 1 | 1 | 1 | 47 | `extracted` |
| `JcwT5rvhXIc` | `youtube_watch_metadata_comments` | `no_extraction_eligible_sources` | 0 | 0 | 0 | 0 | `` |
| `Ln1LUflj8d0` | `youtube_captions+youtube_watch_metadata_comments` | `complete` | 1 | 1 | 1 | 89 | `extracted` |
| `MN3AI-mrPWk` | `youtube_captions+youtube_watch_metadata_comments` | `complete` | 1 | 1 | 1 | 31 | `extracted` |
| `Tb-_V-JVNfk` | `youtube_captions+youtube_watch_metadata_comments` | `complete` | 1 | 1 | 1 | 53 | `extracted` |
| `Uj4bVTM6dm8` | `youtube_captions+youtube_watch_metadata_comments` | `complete` | 1 | 1 | 1 | 53 | `extracted` |
| `VOGZUccarFc` | `youtube_captions+youtube_watch_metadata_comments` | `complete` | 1 | 1 | 1 | 29 | `extracted` |
| `WEqUWKA4FUI` | `youtube_captions+youtube_watch_metadata_comments` | `complete` | 1 | 1 | 1 | 63 | `extracted` |
| `WcSRnnwSAJM` | `youtube_captions+youtube_watch_metadata_comments` | `complete` | 1 | 1 | 1 | 49 | `extracted` |
| `XDscn2sgW3w` | `youtube_captions+youtube_watch_metadata_comments` | `complete` | 1 | 1 | 1 | 45 | `extracted` |
| `_Gp2AmN74E8` | `youtube_captions+youtube_watch_metadata_comments` | `complete` | 1 | 1 | 1 | 47 | `extracted` |
| `as7hye0qgYc` | `youtube_watch_metadata_comments` | `no_extraction_eligible_sources` | 0 | 0 | 0 | 0 | `` |
| `bPJCH9iQUhI` | `youtube_captions+youtube_watch_metadata_comments` | `complete` | 1 | 1 | 1 | 55 | `extracted` |
| `ekaQONEC2ys` | `youtube_captions+youtube_watch_metadata_comments` | `complete` | 1 | 1 | 1 | 93 | `extracted` |
| `hfyoVdOAYt4` | `youtube_captions+youtube_watch_metadata_comments` | `complete` | 1 | 1 | 1 | 17 | `extracted` |
| `jo03W7cBwBM` | `youtube_captions+youtube_watch_metadata_comments` | `complete` | 1 | 1 | 1 | 35 | `extracted` |
| `ljZ7_JHXNdw` | `youtube_captions+youtube_watch_metadata_comments` | `complete` | 1 | 1 | 1 | 37 | `extracted` |
| `rmDwkTrzNxo` | `youtube_captions+youtube_watch_metadata_comments` | `complete` | 1 | 1 | 1 | 105 | `extracted` |
| `sy-rczzFrYg` | `youtube_captions+youtube_watch_metadata_comments` | `complete` | 1 | 1 | 1 | 47 | `extracted` |
| `uaCSynFfPpc` | `youtube_captions+youtube_watch_metadata_comments` | `complete` | 1 | 1 | 1 | 75 | `extracted` |
| `vl-QUTwtneY` | `youtube_captions+youtube_watch_metadata_comments` | `complete` | 1 | 1 | 1 | 61 | `extracted` |
| `vtwo-iaOszA` | `youtube_captions+youtube_watch_metadata_comments` | `complete` | 1 | 1 | 1 | 55 | `extracted` |
| `xK8bmugSpgQ` | `youtube_captions+youtube_watch_metadata_comments` | `complete` | 1 | 1 | 1 | 43 | `extracted` |
| `xZ6vd9fyBbw` | `youtube_captions+youtube_watch_metadata_comments` | `complete` | 1 | 1 | 1 | 113 | `extracted` |

## Claim Levels

| Claim | Status | Basis |
| --- | --- | --- |
| YouTube caption-route source/caption corpus is statistically measurable | observed | 31 videos with both watch metadata/comments and caption transcript packets |
| YouTube caption-route behavioral projection completion is statistically measurable | observed | 31 of 31 caption-ready videos project `complete` after source-lineage-bearing product extraction records |
| YouTube operator/Codex product-extraction records are parser-guarded | observed | 108 batch mentions plus 2 leading-dash retry mentions accepted by `parse_mentions(...)`, 0 rejected, 29 follow-up record sets written |
| YouTube live provider-API extraction is measured | not observed | no provider API key/config was present; records are explicitly labeled operator/Codex |
| YouTube ASR/no-caption route is statistically measurable | not observed | attempted ASR seed is currently unavailable; no complete ASR transcript packet observed |
| YouTube platform-wide behavioral completeness is statistically measurable | not proven | corpus is seed-biased and missing ASR/provider-extraction coverage |
| IG/YT platform-wide behavioral completeness is proven | not proven | IG residuals remain and YouTube ASR/no-caption remains incomplete |

## Next Non-Admin Steps

1. Replace the stale ASR seed with reachable ASR/no-caption candidates and capture at least 5,
   ideally 10, complete ASR transcript cases before claiming fallback-route measurement.
2. Decide whether the current lane accepts operator/Codex parser-guarded extraction as sufficient
   caption-route behavioral evidence, or requires a provider-API rerun when credentials exist.
3. Keep the leading-dash argv normalization covered in runner tests so future batches can pass `--video-id -...` without special quoting.
4. Rerun this receipt after ASR expansion; only then set a platform-level behavioral-completeness
   threshold such as per-route completion rate and residual ceilings.

## Non-Claims

- Not platform-wide YouTube behavioral completeness.
- Not ASR/no-caption fallback validation.
- Not live provider-API extraction.
- Not random or platform-wide YouTube measurement.
- Not shared IG/YT core, production readiness, scheduler behavior, Judgment, or gold verdict.
