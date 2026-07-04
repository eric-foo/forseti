# Aphrodite Depth Rehearsal — Frozen Input Corpus v0

```yaml
retrieval_header_version: 1
artifact_role: Research record (rehearsal input corpus — evidence lane, not product authority)
scope: >
  The frozen input corpus for the Aphrodite single-creator depth rehearsal:
  12 attributed jeremyfragrance Instagram reels with committed transcript and
  page-1 comment records in the Orca data lake, each with verified capture
  provenance (derived record -> bronze-catalog facet row -> raw grid packet
  manifest + sha256 + session identity). Every derived claim in the rehearsal
  binds its source_refs to rows in this corpus. Excludes 4 unattributable
  anchors and the 3 hyram reels by design.
use_when:
  - Resolving the source_refs of any aphrodite_depth_rehearsal_* derived claim.
  - Checking what content the depth rehearsal did and did not run over.
authority_boundary: retrieval_only
open_next:
  - docs/research/aphrodite_depth_rehearsal_extraction_recipe_v0.md
  - docs/research/aphrodite_depth_rehearsal_grade_v0.md
stale_if:
  - The lake records named below are moved, restamped, or superseded.
  - A fuller jeremyfragrance capture supersedes this corpus for rehearsal use.
```

## Status

`FROZEN_REHEARSAL_CORPUS` — assembled 2026-07-04 under the depth-layer build
handoff's recommended first slice (`docs/prompts/handoffs/aphrodite_depth_layer_build_handoff_v0.md`,
authored on branch `claude/aphrodite-depth-prep`), executed under owner
build-authorization granted in-turn on 2026-07-04. Evidence lane only: not
validation, not readiness, not capture authorization, `product_learning`-capped.

## Attribution chain (verified 2026-07-04)

1. **Registry**: `jeremyfragrance` is one of 3 Instagram accounts in
   `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_index_v0.json`.
2. **Raw grid packets** (both manifests contain `instagram.com/jeremyfragrance`;
   verified by direct read):
   - `raw/67c/01KW9T5SGKBYD8HRVP3154F4Y8` — session `ig-live-20260629-jeremyfragrance`,
     capture 2026-06-29T13:47:50Z, manifest sha256
     `4a5360e088a18f8bedcb50418bafa704c12a695a0834b7b80da3d3d7fee2cbcb`.
   - `raw/f00/01KWA193403TYNTBJVWAP5W5NE` — session `01KWA1934R3YMZFMQ4SMNBQ4Q1`,
     capture 2026-06-29T15:51:58Z, manifest sha256
     `c637be6f89c03c383529ebf8f37bbe5cf76c1746dae98db98a56577cbee632cb`.
3. **Bronze catalog facet rows** (`indexes/derived_retrieval/bronze_catalog/v0/by_facet/content__*/instagram_shortcode__*/`)
   join each shortcode below to those raw packets.
4. **Derived deep-capture records** (`derived/<shard>/<shortcode>/silver__capture__{reel_transcript,audience_comments}/`)
   carry the content; each pair's sha256 was recomputed 2026-07-04 and matched
   the packet's `silver__capture__reel_deep_capture__set` record (`member_sha256`)
   for all 12 reels (24/24 hash checks passed).
5. **Content corroboration**: reel `DaH3L1Isdrc` transcript self-identifies the
   creator ("Jim Fraganz here the number one fragrance icon", ASR of Jeremy
   Fragrance; "My fragrance brand fragrance one" — Fragrance One is his brand).

All lake paths are relative to the lake root (locally `F:\orca-data-lake`,
resolved via `ORCA_DATA_ROOT`).

## The corpus (12 reels)

| # | Shortcode | Shard | Posted (UTC) | Transcript posture | Cues | Words | Page-1 comments | Grid comments | Likes | Plays | Transcript sha256 (12) | Comments sha256 (12) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | DaGUhsKsYL9 | 288 | 2026-06-27T18:07 | transcribed | 9 | 32 | 5 | 5 | 209 | 53,399 | `0587b8501ece` | `5bb08c99fe27` |
| 2 | DaH3L1Isdrc | aa3 | 2026-06-28T08:31 | transcribed | 22 | 137 | 14 | 14 | 397 | 32,553 | `d1c27d982c27` | `8a8d3114c440` |
| 3 | DaINMZCCb6N | 6c5 | 2026-06-28T11:44 | transcribed | 28 | 194 | 4 | 4 | 141 | 31,822 | `a47ca757f30e` | `52744de84589` |
| 4 | DaIr5aRsp8p | c7c | 2026-06-28T16:08 | transcribed | 1 | 3 | 15 | 215 | 2,569 | 156,255 | `ac97d402ab8b` | `e92bef8bbeca` |
| 5 | DaK3uKxBlKy | d15 | 2026-06-29T12:33 | no_speech | 0 | 0 | 10 | 16 | 110 | 2,878 | `159c6df43844` | `c3e976da5bf8` |
| 6 | DaKd8E9skt8 | 8c0 | 2026-06-29T08:45 | transcribed | 13 | 54 | 0 | 0 | 96 | 3,153 | `869e05b00122` | `2592e45bff47` |
| 7 | DaKeXcVM0sx | 1dc | 2026-06-29T08:50 | no_speech | 0 | 0 | 10 | 10 | 154 | 4,981 | `699866669f1d` | `3a24f1b87211` |
| 8 | DaKkwCiB_2B | 638 | 2026-06-29T09:46 | no_speech | 0 | 0 | 3 | 3 | 93 | 2,813 | `7b34b6227143` | `9ff3b572e454` |
| 9 | DaKkXGQBE9i | 1de | 2026-06-29T09:42 | transcribed | 9 | 37 | 3 | 4 | 129 | 8,533 | `4639998864c9` | `21bee77e94cc` |
| 10 | DaLBhRbskFa | 6e2 | 2026-06-29T13:56 | transcribed | 3 | 21 | 4 | 4 | 76 | 1,873 | `4784cd58454b` | `67a484ea4564` |
| 11 | DaLBRQiMJhQ | 684 | 2026-06-29T13:54 | transcribed | 5 | 18 | 8 | 8 | 129 | 4,643 | `942040a0b964` | `5354b179e9db` |
| 12 | DaLK8b9s9z9 | f90 | 2026-06-29T15:19 | transcribed | 9 | 97 | 9 | 5 | 54 | 1,584 | `2cb7f3e0ebe9` | `bafa32c5f58c` |

Totals: 9/12 reels with transcribed speech (593 transcript words), 85 page-1
comments. Full 64-hex hashes are in the derived-claims JSON
(`docs/research/aphrodite_depth_rehearsal_derived_claims_v0.json`, `corpus`
block); the 12-hex prefixes above are display truncations of those values.
Grid metadata (caption, likes, plays, paid-partnership flags, timestamps) comes
from packet `01KWA193403TYNTBJVWAP5W5NE`'s
`raw/01_ig_reels_grid_capture.json`.

## Exclusions

- `DaA8n7EhqTR`, `DaK3va8MYT_`, `DaKeK7vMoR0`, `DZ69knlsDb1` — deep-capture
  records exist but no bronze-catalog facet row attributes them to any capture
  session; unattributable content is excluded rather than guessed
  (`DaKeK7vMoR0` is additionally empty: 0 cues, 0 comments).
- `DC9vnmgJWPf`, `DEntAFPpiCv`, `DF3CdyJv79A` — attributed to `hyram`
  (sessions `ig-live-20260629-hyram`, `01KW9T6RC08TB5T84EDMSR1MVM`); out of
  scope for a single-creator rehearsal.

## Named limitations (travel with every downstream claim)

- **Single capture cycle** (one week of reels, captured 2026-06-29): no time
  axis; momentum/trajectory claims impossible.
- **Recent-window stratum only**: no top-K all-time, no breakout-trigger pulls
  (charter Section 6 strata b–d absent).
- **Page-1 comments only**: reel 4 shows the skew concretely — 15 of 215
  comments visible (~7%); moderation invisible; superfan/early skew unmeasured.
- **Short-form ASR quality**: German/English code-switching, entity mangling
  ("Jim Fraganz", "Savage", "Jean Procté"), several cues garbled; reel 3's
  transcript is largely unusable ASR noise despite 28 cues.
- **IG Reels only**: no YouTube long-form content exists in the lake for this
  creator; short-form is not representative of long-form review discourse.

## Non-claims

- Not validation, readiness, buyer proof, or capture authorization.
- Not a roster, registry, or monitoring-policy change.
- Not evidence-grade for any sold report (materiality-reacquisition rule and
  FLAG 1 commercial-use/data-rights gate both remain open).
