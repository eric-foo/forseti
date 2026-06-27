# YouTube Shorts Fragrance Tone Fixture Candidates v0

```yaml
retrieval_header_version: 1
artifact_role: Review input / fixture candidate scout
scope: Thirty verified public YouTube Shorts candidates from fragrance creators for the rhetorical-tone fixture spike.
use_when:
  - Selecting candidate YouTube Shorts for transcript-based rhetorical-tone fixture authoring.
  - Checking which fragrance creator Shorts were found by the bounded YouTube capture-spine route.
authority_boundary: retrieval_only
open_next:
  - docs/review-inputs/youtube_shorts_fragrance_tone_fixture_candidates_v0.json
  - orca/product/spines/capture/core/source_families/social_media/youtube/youtube_capture_recon_v0.md
  - orca/product/spines/capture/core/source_families/social_media/youtube/youtube_capture_agent_playbook_v0.md
```

## Summary

- Candidate count: 30
- Creator distribution: JeremyFragrance=3, GentsScents=3, ThePerfumeGuy=3, SchoolofScent=3, CurlyScents=3, funmimonet=3, SokiLondon=3, TLTGReviews=3, Redolessence=3, TheFragranceApprentice=3
- Route: public @handle/shorts enumeration + /shorts/<id> serving-surface verification + /watch metadata
- Network backend: `curl_cffi:chrome`
- Retrieval time UTC: `2026-06-26T08:29:59.565404Z`
- Raw scout JSON: `docs/review-inputs/youtube_shorts_fragrance_tone_fixture_candidates_v0.json`
- Raw scout JSON SHA256: `860cd06c0276da241f5b4555e81ec2034d143f8b7b58e94e038ee0269b83f6fc`

## Selection Boundary

These are **candidate inputs**, not admitted fixtures. Each item was found through a public `@handle/shorts` page, verified by requesting `/shorts/<video_id>` and checking that the serving surface stayed on `/shorts/`, then enriched with `/watch?v=<video_id>` metadata. The relevance filter required a fragrance/perfume/cologne/scent-related title keyword.

## Non-Claims

- not packet-grade SourceCapturePacket output
- not transcript capture
- not ASR
- not tone labels
- not fixture admission
- not validation or readiness
- comments not captured
- surface verified from serving behavior, but Shorts identity should still travel as source-context evidence in any downstream record

## Candidates

| # | Creator handle query | Video ID | Shorts URL | Length (s) | Publish date | Title |
| --- | --- | --- | --- | ---: | --- | --- |
| 1 | `JeremyFragrance` | `as7hye0qgYc` | [https://www.youtube.com/shorts/as7hye0qgYc](https://www.youtube.com/shorts/as7hye0qgYc) | 16 | 2026-06-26T01:09:58-07:00 | UNIQUE BLUE, By SUPERZ: #jeremyfragrance #fragrance #cologne #perfume #parfum |
| 2 | `JeremyFragrance` | `t4mAPmthgO0` | [https://www.youtube.com/shorts/t4mAPmthgO0](https://www.youtube.com/shorts/t4mAPmthgO0) | 17 | 2026-06-26T01:09:14-07:00 | FRAGRANCE Video: #jeremyfragrance #fragrance #cologne #perfume #parfum |
| 3 | `JeremyFragrance` | `s7F2VDKEIPk` | [https://www.youtube.com/shorts/s7F2VDKEIPk](https://www.youtube.com/shorts/s7F2VDKEIPk) | 40 | 2026-06-26T01:08:28-07:00 | final70 70% FRAGRANCE Discount, At 700USD/EUR at www.fragrance.one #jeremyfragrance #fragrance |
| 4 | `GentsScents` | `ljZ7_JHXNdw` | [https://www.youtube.com/shorts/ljZ7_JHXNdw](https://www.youtube.com/shorts/ljZ7_JHXNdw) | 54 | 2023-03-23T15:12:41-07:00 | Ultra Male For Ultra Cheap - Lattafa Ramz Silver |
| 5 | `GentsScents` | `VOGZUccarFc` | [https://www.youtube.com/shorts/VOGZUccarFc](https://www.youtube.com/shorts/VOGZUccarFc) | 52 | 2023-03-18T11:30:33-07:00 | Top 10 Spring Designer Fragrances For Men 2023 |
| 6 | `GentsScents` | `sy-rczzFrYg` | [https://www.youtube.com/shorts/sy-rczzFrYg](https://www.youtube.com/shorts/sy-rczzFrYg) | 58 | 2023-03-13T12:00:20-07:00 | The Best Blue Fragrances For The Classy Modern Man |
| 7 | `ThePerfumeGuy` | `rmDwkTrzNxo` | [https://www.youtube.com/shorts/rmDwkTrzNxo](https://www.youtube.com/shorts/rmDwkTrzNxo) | 119 | 2025-10-30T17:30:56-07:00 | $88 for the BEST La Vie Est Belle Flanker?! 😍 |
| 8 | `ThePerfumeGuy` | `5QDcTenklxg` | [https://www.youtube.com/shorts/5QDcTenklxg](https://www.youtube.com/shorts/5QDcTenklxg) | 90 | 2025-10-28T17:30:09-07:00 | The Best Fruity Oud You’re Not Wearing! |
| 9 | `ThePerfumeGuy` | `hfyoVdOAYt4` | [https://www.youtube.com/shorts/hfyoVdOAYt4](https://www.youtube.com/shorts/hfyoVdOAYt4) | 90 | 2025-10-26T17:29:46-07:00 | $25 Men’s Fragrance That Smells Like Luxury \| Bentley for Men Intense 👑 |
| 10 | `SchoolofScent` | `vl-QUTwtneY` | [https://www.youtube.com/shorts/vl-QUTwtneY](https://www.youtube.com/shorts/vl-QUTwtneY) | 53 | 2026-06-25T07:13:18-07:00 | The Best Summer Fragrance For Each Age Group |
| 11 | `SchoolofScent` | `WEqUWKA4FUI` | [https://www.youtube.com/shorts/WEqUWKA4FUI](https://www.youtube.com/shorts/WEqUWKA4FUI) | 56 | 2026-06-24T08:52:53-07:00 | The Highest Rated Summer Fragrances At Each Price Range |
| 12 | `SchoolofScent` | `uaCSynFfPpc` | [https://www.youtube.com/shorts/uaCSynFfPpc](https://www.youtube.com/shorts/uaCSynFfPpc) | 67 | 2026-06-23T05:55:38-07:00 | This Fragrance Or SHL God Of Fire? - Mykonos Perfume Top 3 Buying Guide |
| 13 | `CurlyScents` | `t2ZqtfUc56k` | [https://www.youtube.com/shorts/t2ZqtfUc56k](https://www.youtube.com/shorts/t2ZqtfUc56k) | 27 | 2026-03-19T08:26:16-07:00 | Turning my scent of the day into a VIDEO GAME! 👾 🎮 |
| 14 | `CurlyScents` | `MN3AI-mrPWk` | [https://www.youtube.com/shorts/MN3AI-mrPWk](https://www.youtube.com/shorts/MN3AI-mrPWk) | 35 | 2026-03-15T07:55:58-07:00 | Top 10 Best Spring Perfumes for WOMEN. |
| 15 | `CurlyScents` | `FqTrOZbh_DE` | [https://www.youtube.com/shorts/FqTrOZbh_DE](https://www.youtube.com/shorts/FqTrOZbh_DE) | 29 | 2026-03-05T07:54:50-08:00 | TOP 10 SEXIEST SPRING FRAGRANCES FOR MEN! |
| 16 | `funmimonet` | `bPJCH9iQUhI` | [https://www.youtube.com/shorts/bPJCH9iQUhI](https://www.youtube.com/shorts/bPJCH9iQUhI) | 57 | 2026-06-15T15:53:42-07:00 | #DovePartner The best smelling skin on the block starts with @dove Serum+ Oil Body Wash |
| 17 | `funmimonet` | `Uj4bVTM6dm8` | [https://www.youtube.com/shorts/Uj4bVTM6dm8](https://www.youtube.com/shorts/Uj4bVTM6dm8) | 45 | 2025-04-07T19:17:59-07:00 | Notes Shanghai 2025 #notesshanghai #perfume #notesshanghai2025 #fragrance |
| 18 | `funmimonet` | `ddGipRGnWrI` | [https://www.youtube.com/shorts/ddGipRGnWrI](https://www.youtube.com/shorts/ddGipRGnWrI) | 33 | 2024-08-05T16:45:02-07:00 | How I safely packed 48lbs of perfume back to the US #perfumecollection #nicheperfume |
| 19 | `SokiLondon` | `XDscn2sgW3w` | [https://www.youtube.com/shorts/XDscn2sgW3w](https://www.youtube.com/shorts/XDscn2sgW3w) | 56 | 2026-06-25T02:39:18-07:00 | Which Is The Best Version Of The New CK Euphoria Elixir Perfumes...? \| Soki London |
| 20 | `SokiLondon` | `Rxufi0kOFaM` | [https://www.youtube.com/shorts/Rxufi0kOFaM](https://www.youtube.com/shorts/Rxufi0kOFaM) | 11 | 2026-06-15T05:13:50-07:00 | Cleopatra was a finalist last week for Best Fragrance 2026 💛 👑  \| Soki London |
| 21 | `SokiLondon` | `Fd-aChpt_Ss` | [https://www.youtube.com/shorts/Fd-aChpt_Ss](https://www.youtube.com/shorts/Fd-aChpt_Ss) | 34 | 2026-06-08T06:20:51-07:00 | @EmiBudhabhai Tries The Soki London Ophelia Travel Spray 🌸❤️ |
| 22 | `TLTGReviews` | `7S40eU8FDCY` | [https://www.youtube.com/shorts/7S40eU8FDCY](https://www.youtube.com/shorts/7S40eU8FDCY) | 48 | 2026-06-24T12:33:43-07:00 | Spectrum Chill is definitely one of THE BEST Clone Releases of 2026 |
| 23 | `TLTGReviews` | `-V7MN2IWMpA` | [https://www.youtube.com/shorts/-V7MN2IWMpA](https://www.youtube.com/shorts/-V7MN2IWMpA) | 177 | 2026-06-21T07:06:00-07:00 | The Fragrance to Celebrate a Successful Show |
| 24 | `TLTGReviews` | `Ln1LUflj8d0` | [https://www.youtube.com/shorts/Ln1LUflj8d0](https://www.youtube.com/shorts/Ln1LUflj8d0) | 90 | 2026-06-15T15:27:01-07:00 | Lattafa Khamrah Waha can be worn in ANY SEASON! |
| 25 | `Redolessence` | `JMmEIv_oG4o` | [https://www.youtube.com/shorts/JMmEIv_oG4o](https://www.youtube.com/shorts/JMmEIv_oG4o) | 55 | 2026-06-25T20:24:31-07:00 | Rasasi Hawas Reina Perfume Review! |
| 26 | `Redolessence` | `_Gp2AmN74E8` | [https://www.youtube.com/shorts/_Gp2AmN74E8](https://www.youtube.com/shorts/_Gp2AmN74E8) | 50 | 2026-06-25T17:17:21-07:00 | Stallion 53 Donna Intense Perfume Review! |
| 27 | `Redolessence` | `Tb-_V-JVNfk` | [https://www.youtube.com/shorts/Tb-_V-JVNfk](https://www.youtube.com/shorts/Tb-_V-JVNfk) | 60 | 2026-06-25T14:16:38-07:00 | House of Dastan Love Flame Perfume Review! |
| 28 | `TheFragranceApprentice` | `6k8ebJw50tU` | [https://www.youtube.com/shorts/6k8ebJw50tU](https://www.youtube.com/shorts/6k8ebJw50tU) | 37 | 2025-04-14T11:09:41-07:00 | 5th September 2026 will be the end of the Fragrance Apprentice |
| 29 | `TheFragranceApprentice` | `5e4y5yNagRI` | [https://www.youtube.com/shorts/5e4y5yNagRI](https://www.youtube.com/shorts/5e4y5yNagRI) | 19 | 2023-12-16T08:51:42-08:00 | I STILL forbid you to buy this fragrance. |
| 30 | `TheFragranceApprentice` | `WcSRnnwSAJM` | [https://www.youtube.com/shorts/WcSRnnwSAJM](https://www.youtube.com/shorts/WcSRnnwSAJM) | 55 | 2023-12-10T07:00:21-08:00 | The Fragrance That Smells of Christmas and Horse Poop |

## Suggested Next Step

Run caption-first transcript acquisition on this candidate set and keep the first 30 usable transcript fixtures only if quote/timestamp binding succeeds. If captions are missing, use the existing ASR fallback path, but keep `transcript_source` and input posture explicit.
