# Capture Source Family: YouTube

```yaml
retrieval_header_version: 1
artifact_role: Capture source-family lane index
scope: >
  Cold-start lane index for YouTube public watch/Shorts metadata, comments,
  captions/ASR, creator observation, metric rollup, and transcript-product
  downstream seams.
use_when:
  - Starting or reviewing YouTube public capture, transcript, metric, or creator-observation work.
  - Routing a "capture YouTube" request from the Source Capture Playbook into source-specific docs and runners.
  - Checking which YouTube artifacts are Capture-owned versus Cleaning/Data Lake/Creator Signal consumers.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/social_media/youtube/youtube_capture_agent_playbook_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/youtube/youtube_capture_recon_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/youtube/youtube_video_capture_surface_findings_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/youtube/youtube_transcript_product_extraction_spec_v0.md
  - forseti/product/spines/data_lake/README.md
stale_if:
  - YouTube served-HTML embedded state, youtubei comments route, caption/ASR packet route, or po_token posture changes.
  - YouTube watch/caption/ASR packet runners, metric rollup producers, or transcript-product Cleaning lane changes.
  - Data Lake or Silver authority changes the raw/derived/Silver seam.
```

## Canonical Route Home

Open `youtube_capture_agent_playbook_v0.md` first for YouTube run posture and
`youtube_capture_recon_v0.md` for route evidence. This README is the lane map.

## Route Map

| Layer | Current home | What to confirm |
| --- | --- | --- |
| Access / method | `youtube_capture_agent_playbook_v0.md`; `youtube_capture_recon_v0.md` | Public-only route; served HTML embedded `ytInitialPlayerResponse`; `youtubei/v1/next` comment continuations; anonymous Chrome-impersonating transport. |
| Watch metadata/comments packet | `forseti-harness/source_capture/youtube_watch_packet.py`; runner `run_source_capture_youtube_watch_packet.py` | Selective-structured SourceCapturePacket writes for source-visible watch metadata, full bounded comment bodies/identity/engagement/order, availability states, metric observations, coverage, and route receipts. Capture v1 does not persist enclosing watch HTML or raw youtubei response bodies; historical v0 packets remain readable. |
| Captions / ASR packets | `orca-harness/source_capture/transcript/youtube_captions.py`; `caption_packet.py`; `asr_packet.py`; runners `run_source_capture_youtube_caption_packet.py`, `run_source_capture_youtube_asr_packet.py` | Raw transcript acquisition and ASR fallback staging; readable product extraction is downstream Cleaning. |
| Creator observations / metric rollups | `youtube_creator_observation_ledger_spec_v0.md`, metric seed/snapshot JSONs; runners `run_youtube_creator_metric_rollup_producer.py`, `run_youtube_watch_packet_metric_rollup_producer.py` | Source-backed creator/channel observations and metric rollups over admitted packets; not cross-platform identity proof. |
| Audience post-text Cleaning seam | `orca-harness/source_capture/audience_post_packet.py`; `orca-harness/cleaning/audience_post_input.py`; `orca-harness/cleaning/audience_extractor.py`; `docs/prompts/handoffs/youtube_post_ecr_cleaning_adapter_architecture_handoff_v0.md` | Post-text packets use the platform as `source_family` and `youtube_post_text` as the source surface; the deterministic adapter feeds Pass-1 audience extraction and is not a fake top-level source family. |
| Transcript product extraction | `youtube_transcript_product_extraction_spec_v0.md`; `orca-harness/cleaning/transcript_product_lake.py`; runner `run_transcript_product_extract.py` | Cleaning/Silver product-mention lane over committed transcripts; not Capture authority or Judgment. |
| Data Lake authority | `forseti/product/spines/data_lake/README.md` -> `authority/` | Raw admission, path grammar, derived layout, and Silver semantics. |

## Current Posture

YouTube long-form and Shorts share a source-family route for public metadata and
comments. The default deep-capture packet retains one source-default-order comment
page as selected structured Bronze and records the discarded response-envelope
posture explicitly. Captions and ASR are separate acquisition routes into raw
artifacts; downstream readable/clean product mentions belong to Cleaning/Silver.

## Non-Claims

Not validation, readiness, live capture authorization, platform-wide coverage,
bot/fake classification, product/Judgment proof, commercial-readiness evidence,
or legal advice. Dislikes are not public ground truth unless a separate
creator-consent/OAuth route is supplied.
