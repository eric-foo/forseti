# TikTok Funmi N30 Comment Subtitle Cadence Analysis v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow analysis receipt
scope: >
  Analysis of the 30 Funmi Monet TikTok videos captured in the 2026-06-30
  sessioned cadence pilot: profile/list metadata, page-owned comment-list
  packet fields, source-native subtitle/WebVTT coverage, disclosure/source-text
  signals, and first-pass audience behavior signals.
use_when:
  - Deciding what to do next with the 30 captured TikTok videos.
  - Checking whether the TikTok per-video comment/subtitle route has enough
    evidence to move from live probing to durable packetization and extraction.
  - Avoiding another same-creator capture rung before the captured batch is
    analyzed and admitted.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/tiktok_behavioral_gap_ledger_from_ig_youtube_v0.md
  - docs/workflows/tiktok_behavioral_sync_fresh_lane_handoff_v0.md
  - orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
  - orca-harness/source_capture/tiktok/admission.py
  - orca-harness/source_capture/tiktok/video_packet.py
stale_if:
  - The referenced F-lake staging result files are deleted, moved, or rewritten.
  - A later TikTok batch changes the comment route rate, subtitle route rate, or
    challenge/cooldown posture.
  - The TikTok parser/admission packet contract changes materially.
```

## Confirm-Don't-Trust Load Outcome

Outcome: `PARTIAL_REUSE`.

Cleanly reverified for the original analysis checkpoint:

- Worktree checkpoint: `codex/ig-youtube-residual-burndown-pushable` at
  `2457f816307e59985aa3161cd5da3baa2401c006`; clean against origin at the time
  of this analysis.
- The packet's load-bearing source hashes matched for `AGENTS.md`, overlay
  source-loading/routing/source-of-truth/artifact/retrieval sources, the TikTok
  prior handoff, gap ledger, sessioned DOM receipt/payload, capture playbook,
  recon index, TikTok capture spec, first-slice recon, and warm-probe plan.
- The F-lake staging result files below were fresh-read directly.
- Later durable batch admission follow-up in this file was added at
  `163eb76706e1029347936572c25207fb4de64a92`; use that follow-up section for
  the current packetized admission state.

Why partial rather than full reuse:

- The fresh-lane handoff's original next action was pinned response-body proof;
  that state is superseded by later same-lane evidence: N=1, then N=5, then
  N=25 remaining captured page-owned comment-list bodies and subtitle candidates.
- Some older source docs still say TikTok transcript/source-native subtitle
  behavior is unproven. This receipt narrows that: source-native WebVTT is
  measured for the Funmi N=30 batch when `subtitleInfos` exists; cross-creator
  coverage and long-run account survivability remain unproven.

## Evidence Files

| Evidence | Path | SHA256 |
| --- | --- | --- |
| Profile/grid response | `F:\orca-data-lake\.staging\tiktok_funmi_grid_response_probe_20260630T145319Z\result.json` | `DFFB126AC01525289338F7E780016D2245B539459575A7052DF9E4FEF873671A` |
| N=5 cadence pilot | `F:\orca-data-lake\.staging\tiktok_funmi_n5_comment_subtitle_cadence_probe_20260630T165301Z\result.json` | `A25B625D7738D510C146E02E2DCAB403313F11450D8312A0EA88F151721CFBA4` |
| N=25 remaining cadence rung | `F:\orca-data-lake\.staging\tiktok_funmi_n25_remaining_comment_subtitle_cadence_probe_20260630T170246Z\result.json` | `BEBB5A2B9B63CD654DED43A7D95E3D9CCEE924D5C5796333AFBA3081F6A7F67B` |

The grid response contains extra `/api/repost/item_list/` items from other
authors. This analysis filters by the 30 captured Funmi video IDs.

## Capture QA Result

| Check | Observed result | Interpretation |
| --- | --- | --- |
| Batch size | 30 attempted, 30 completed, 0 failed | The Funmi/session path is clean at N=30. |
| Challenge/block markers | 0 challenges across 30 | Good batch signal; not a long-run account ceiling. |
| Cadence | N=5 used 45-75s sleep; N=25 used 75-120s sleep | Conservative enough for this rung; do not infer optimal cadence. |
| Comment route | 30/30 videos produced one page-owned `/api/comment/list` response | Packet-grade comment body route measured for this creator/session. |
| Comment fields | Captured comments carried `cid`, `text`, `create_time`, `digg_count`, `reply_comment_total`, `user.uid`, `user.unique_id`, `user.nickname`, source order, body hash, envelope `cursor`, `has_more`, and `total` | Meets the TikTok comment packet contract for first-page top/relevant comments. |
| Comment volume | 596 parsed comments from envelope totals summing to 4,255 | This is a first-page sample, not a full census. |
| Subtitle metadata | 26/30 videos had `subtitleInfos`; 4/30 had no subtitle metadata | Subtitle denominator should be `metadata present`, not all videos. |
| Subtitle body route | 26/26 videos with `subtitleInfos` fetched/parsing WebVTT successfully | Source-native subtitle route is measured when metadata is present. |
| Subtitle cue volume | 1,044 parsed WebVTT cues across 26 videos | Enough for extraction; still source-native ASR/caption text, not owner ASR. |
| Content-Type caveat | Subtitle fetch summaries can report `video/mp4` while body parses as WebVTT | Validate body shape plus metadata, not response content type alone. |
| Secret hygiene | Staging contracts record no cookie/token/storage persistence, no raw endpoint URLs, no raw subtitle URLs, no raw response bodies | Raw material remains excluded; parsed public text and hashes are admitted. |

## Coverage Table

| # | Date UTC | Video ID | Views | Likes | Comment total | Captured comments | Subtitle | Disclosure/source-text signal |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| 00 | 2026-06-25 | `7655162561783975199` | 10,800 | 1,625 | 96 | 20 | 23 cues | none observed |
| 01 | 2026-06-23 | `7654667917811797279` | 43,000 | 5,936 | 231 | 20 | 64 cues | none observed |
| 02 | 2026-06-22 | `7654358000114830623` | 4,991 | 776 | 189 | 20 | 34 cues | none observed |
| 03 | 2026-06-19 | `7653179416184491295` | 15,300 | 1,949 | 96 | 20 | 23 cues | none observed |
| 04 | 2026-06-17 | `7652163228734197022` | 9,612 | 1,223 | 108 | 20 | 77 cues | none observed |
| 05 | 2026-06-15 | `7651732163511012638` | 5,954 | 567 | 58 | 19 | 25 cues | `#DovePartner`; transcript says partnered with Dove |
| 06 | 2026-06-15 | `7651406215867551006` | 7,111 | 910 | 52 | 20 | no `subtitleInfos` | none observed |
| 07 | 2026-06-14 | `7651396713919368479` | 13,100 | 2,240 | 107 | 19 | 96 cues | none observed |
| 08 | 2026-06-05 | `7648062475006463262` | 20,500 | 2,974 | 129 | 20 | 55 cues | none observed |
| 09 | 2026-05-31 | `7645891981427707167` | 11,400 | 1,466 | 88 | 20 | no `subtitleInfos` | none observed |
| 10 | 2026-05-30 | `7645801214004825374` | 11,100 | 1,540 | 111 | 20 | no `subtitleInfos` | none observed |
| 11 | 2026-05-29 | `7645390188352408863` | 17,100 | 2,682 | 303 | 20 | 95 cues | PR/unboxing source text |
| 12 | 2026-05-28 | `7645012202616818974` | 18,700 | 2,289 | 99 | 20 | 50 cues | none observed |
| 13 | 2026-05-26 | `7644326029036670239` | 13,300 | 1,638 | 88 | 19 | 29 cues | none observed |
| 14 | 2026-05-22 | `7642848016650620190` | 11,900 | 1,262 | 71 | 20 | 19 cues | Brown Sugar Babe launch/source text |
| 15 | 2026-05-18 | `7641286244860726559` | 804,800 | 967 | 48 | 20 | 28 cues | `#eospartner` |
| 16 | 2026-05-15 | `7640214811187449118` | 7,632 | 710 | 63 | 20 | 33 cues | `#ad`; Burberry launch/source text |
| 17 | 2026-05-12 | `7639063958237760782` | 41,700 | 5,999 | 332 | 19 | no `subtitleInfos` | none observed |
| 18 | 2026-05-04 | `7636143114826026271` | 10,400 | 651 | 70 | 20 | 24 cues | `#NYXCosmeticsPartner`; transcript says sponsored by NYX |
| 19 | 2026-05-01 | `7634706760615333150` | 90,400 | 7,905 | 316 | 20 | 17 cues | none observed |
| 20 | 2026-04-30 | `7634571657008467231` | 29,700 | 4,253 | 105 | 20 | 3 cues | none observed |
| 21 | 2026-04-23 | `7632075498926935326` | 31,800 | 4,284 | 138 | 20 | 53 cues | none observed |
| 22 | 2026-04-21 | `7631271803763068191` | 48,800 | 8,280 | 266 | 20 | 87 cues | PR/unboxing source text |
| 23 | 2026-04-17 | `7629774409762442526` | 16,700,000 | 57,600 | 304 | 20 | 15 cues | `#BurberryPartner` |
| 24 | 2026-04-14 | `7628409363471895838` | 26,100 | 2,604 | 58 | 20 | 71 cues | none observed |
| 25 | 2026-04-13 | `7628368083282906398` | 26,200 | 1,920 | 95 | 20 | 14 cues | `#NYXCosmeticsPartner` |
| 26 | 2026-04-11 | `7627293584361917727` | 25,500 | 2,368 | 103 | 20 | 20 cues | none observed |
| 27 | 2026-04-10 | `7626922878700653855` | 20,900 | 2,014 | 84 | 20 | 35 cues | none observed |
| 28 | 2026-04-07 | `7625839445027212574` | 80,500 | 8,225 | 333 | 20 | 35 cues | none observed |
| 29 | 2026-04-01 | `7623876014120160542` | 14,300,000 | 6,838 | 114 | 20 | 19 cues | `#ad`; Calvin Klein/Amazon source text |

## Behavioral Read

This is a first-pass, source-text analysis from grid captions, parsed WebVTT cue
text, and the first page of public comments. It is not Cleaning, Judgment, or a
final product-extraction record.

Core observations:

- The 30-video window runs from 2026-04-01 through 2026-06-25.
- Total grid views sum to 32.46M, but two disclosed posts dominate: Burberry Her
  at 16.7M views and Calvin Klein Euphoria Elixir at 14.3M views. Together they
  account for about 31.0M of 32.46M views. The non-viral 28-video view sum is
  about 1.46M, with median views around 17.9K.
- Median views across all 30 are about 19.6K; median likes about 2.1K; median
  total comments about 104; median saves about 136.
- Source-visible disclosure/ad/partner signals appear on 7/30 videos:
  Dove, EOS, Burberry, NYX, Burberry Her, NYX teaser, and Calvin Klein/Amazon.
  This is source text only unless a platform ad-disclosure field is separately
  captured; do not collapse hashtag/source-text disclosure into TikTok-rendered
  paid-partnership proof.
- Multi-label content mix: routine/layering/bodycare signals appear in 18
  videos; review/recommendation in 10; event/travel/launch context in 13;
  PR/unboxing/haul in 3; industry commentary in 1; partner/ad in 7.
- Audience-intent heuristic over the captured comment sample matched 133/596
  comments, with 65 question-mark comments. This is a cheap signal only; it
  should become a typed extraction pass before product claims.

Brand/source-text recurrence in the 30-video corpus:

- Sephora appears in 7 videos.
- Chris Collins appears in 5 videos.
- EOS, Brown Sugar Babe, Snif, and Soft Services each appear in 3 videos.
- Burberry, NYX, L'Occitane, Pacifica, and twentysecondofmay each appear in 2
  videos.
- Single-video source-text mentions include Dove, Calvin Klein, Amazon, Ulta,
  Armani, Commodity, Kayali, Amouage, Tom Ford, Carolina Herrera, Kilian,
  Suave, Tatcha, Huda, Rare Beauty, Fenty, EX NIHILO, Maison Mataha, and others.

Highest audience-intent rows in the captured top-comment sample:

| Rank signal | Video | Heuristic match |
| --- | --- | --- |
| High intent | Chris Collins mango perfume review (`7627293584361917727`) | 9/20 captured comments matched intent terms; 5 question comments |
| High intent | May PR unboxing (`7645390188352408863`) | 9/20 matched intent terms |
| High intent | Top 10 perfumes (`7654667917811797279`) | 8/20 matched; 6 question comments |
| High intent | Burberry Her partner video (`7629774409762442526`) | 8/20 matched |
| High intent | NYX partner body collection (`7636143114826026271`) | 7/20 matched |

## Decision

Do not spend the next step on more same-creator live capture. The N=30 captured
batch is already enough to move the lane from route proof to durable analysis.

Next move: `DURABLE_PACKETIZATION_AND_EXTRACTION_NEXT`.

Smallest complete sequence:

1. Admit the N=30 staging outputs into a durable, sanitized TikTok batch
   artifact or packet family. Do not rerun the same 30 merely to obtain raw
   response bodies; the batch intentionally preserved hashes, parsed fields, and
   no-secret posture rather than raw bodies.
2. Add a batch admission path that accepts parsed page-owned comment/subtitle
   proofs plus body/subtitle hashes, field coverage, envelope fields, and
   source-lineage, or explicitly document why the single-video SCI runner must
   stay as-is and a new batch receipt writer is required.
3. Run typed extraction over the admitted parsed text: product/brand mentions,
   disclosure/source-text posture, transcript-derived product claims, comment
   intent/question signals, and audience objection/pull themes. Keep it below
   Judgment: no demand score, creator-quality verdict, or buyer-proof claim.
4. Only after durable packetization and extraction are complete should the lane
   spend more TikTok account/session budget. The next live rung should be a
   different creator or a small cross-creator batch, not more Funmi volume.

## Durable Batch Admission Follow-Up (2026-07-01)

The N=30 staging outputs were admitted into a canonical sanitized SourceCapturePacket
without new live TikTok probing.

Fresh-read verified packet:

- Packet path: `F:\orca-data-lake\raw\97c\01KWCYZ9P72W4SJD7NDPRQT0DB`
- Packet id: `01KWCYZ9P72W4SJD7NDPRQT0DB`
- Source surface: `tiktok_creator_batch_comment_subtitle_admission`
- Preserved file: `raw/01_tiktok_batch_capture.json`
- Source input SHA-256 values:
  - grid: `dffb126ac01525289338f7e780016d2245b539459575a7052df9e4fef873671a`
  - N5: `a25b625d7738d510c146e02e2dcab403313f11450d8312a0ea88f151721cfba4`
  - N25: `bebb5a2b9b63cd654ded43a7d95e3d9ccee924d5c5796333afba3081f6a7f67b`

Fresh-read verified batch summary:

- `video_count=30`, `attempted_count=30`, `completed_count=30`, `challenge_count=0`
- `comment_response_success_count=30`, `captured_comment_count=596`, `comment_envelope_total_sum=4255`
- `subtitle_info_video_count=26`, `subtitle_success_count=26`, `subtitle_cue_count=1044`, `transcript_text_available_count=26`
- Grid stats sums admitted from parsed profile/list items: `playCount=32458300`, `diggCount=143695`, `commentCount=4252`, `shareCount=3975`, `collectCount=15331`
- Source-text disclosure heuristic in the admitted typed seed: `source_text_disclosure_video_count=9`
- Fresh read found no raw signed-marker strings among `msToken=`, `X-Bogus=`, or `tiktokcdn` in the preserved payload.

Implementation route now exists:

- `orca-harness/source_capture/tiktok/batch_packet.py`
- `orca-harness/runners/run_source_capture_tiktok_batch_packet.py`
- `orca-harness/tests/unit/test_tiktok_batch_admission.py`

The admitted typed fields are a deterministic extraction seed only: source mentions,
hashtags, disclosure-source-text signals, comment question/intent term counts, and
transcript signal terms. They are not final product extraction, Cleaning, ECR, or
Judgment.

Updated next move: `TYPED_PRODUCT_EXTRACTION_FROM_TIKTOK_BATCH_PACKET_NEXT`.

## Residuals

- This is one creator, one account/session, one short capture window, one
  vertical style. It is not a general TikTok guarantee.
- The batch proves first-page top/relevant comments, not a full comment census,
  reply-thread expansion, or chronological comment windows.
- The subtitle route is `26/26` when `subtitleInfos` exists, and `26/30` over
  all captured videos. The four misses are `no_subtitleInfos_present`, not fetch
  failures.
- Source-native WebVTT is TikTok-provided subtitle/caption text with `Source`
  values such as `ASR`; it is not owner-generated ASR and not durable video or
  audio preservation.
- Raw response bodies, raw signed endpoint URLs, raw subtitle URLs, cookies,
  tokens, storage state, device IDs, proxy endpoints, and exit IPs are not
  persisted. That is correct hygiene, but it means durable admission must be
  designed around parsed proof plus hashes, not raw-body replay.
- Platform-rendered paid-partnership labels were not measured across the N=30
  batch. Hashtag/source-text disclosure signals are source text and should stay
  separate from platform ad-disclosure fields.
- The original result files still live in `F:\orca-data-lake\.staging`; the canonical sanitized batch packet is now `F:\orca-data-lake\raw\97c\01KWCYZ9P72W4SJD7NDPRQT0DB`.

## Non-Claims

Not TikTok validation, production readiness, account safety proof, legal advice,
general creator coverage, cross-creator subtitle coverage, Cleaning, ECR,
Judgment, buyer-proof, or product-verdict proof.
