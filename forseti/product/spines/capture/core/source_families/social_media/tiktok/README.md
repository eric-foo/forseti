# Capture Source Family: TikTok

```yaml
retrieval_header_version: 1
artifact_role: Capture source-family lane index
scope: >
  Cold-start lane index for TikTok public/sessioned creator capture, packet
  admission, batch projection, and current residuals.
use_when:
  - Starting or reviewing TikTok capture-to-lake work.
  - Checking whether TikTok has a landed route, batch packet, projection, or unresolved residual.
  - Routing a "capture TikTok" request from the Source Capture Playbook into the TikTok lane.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/tiktok/tiktok_first_slice_probe_recon_v0.md
  - docs/workflows/tiktok_ui_movement_blocker_substrate_playbook_v0.md
  - docs/workflows/tiktok_funmi_n30_comment_subtitle_cadence_analysis_v0.md
  - forseti/product/spines/data_lake/README.md
stale_if:
  - TikTok sessioned/live runner admission, auth-state provenance, or challenge follow-through posture changes.
  - TikTok batch admission/projection helpers change source_surface, packet, or data-root behavior.
  - Cross-creator coverage, account-safety, durable media, or product extraction moves from residual to landed capability.
```

## Canonical Route Home

For TikTok, the owning source-family route is:

`forseti/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md`

Open that spec before runner use or code review. The Source Capture Playbook owns
the general access-method doctrine; this README is the TikTok lane map.

## Current Route Shape

| Layer | Current home | What to confirm |
| --- | --- | --- |
| Access / method | `tiktok_capture_lane_spec_v0.md`; `tiktok_ui_movement_blocker_substrate_playbook_v0.md` | Sessioned/cookied real-browser posture, no forged signatures, no secret persistence, stop-on-unresolved-challenge, and owner-authorized X-able follow-through boundaries. |
| Live staging | `orca-harness/source_capture/tiktok/live_batch_probe.py`; runner `run_source_capture_tiktok_live_batch_probe.py` | One creator per invocation; headed/sessioned or logged-out page-owned observation; sanitized staging by default. |
| Raw packet admission | `orca-harness/source_capture/tiktok/batch_packet.py`; runner `run_source_capture_tiktok_batch_packet.py` | Network-free parsed-batch admission; explicit `--data-root` / `--admit-output` for lake output; fail closed on challenge/failure/diagnostic markers. |
| Coverage/projection | `orca-harness/source_capture/tiktok/batch_coverage.py`, `batch_projection.py`; runners `run_tiktok_batch_coverage.py`, `run_tiktok_batch_projection.py` | Text-free admitted-batch coverage/projection only; not product extraction, Cleaning, or Judgment. |
| Data Lake authority | `forseti/product/spines/data_lake/README.md` -> `authority/` | Raw admission, path grammar, derived layout, and Silver semantics. Do not restate them here. |

## Current Evidence And Residuals

- TikTok is no longer absent. First-slice recon, sessioned warm/profile/comment
  receipts, a lane spec, and Funmi N30 parsed-batch admission evidence exist.
- Funmi N30 parsed-batch admission is source-specific evidence: 30 videos,
  parsed comments, source-native WebVTT where `subtitleInfos` existed, and
  deterministic typed extraction seeds are recorded in the TikTok sources.
- Remaining residuals include cross-creator coverage, higher-volume account
  safety, durable media/video preservation, full comment census, platform-wide
  subtitle availability, and final product extraction.

## Non-Claims

Not validation, readiness, live capture success for a new account/creator,
source completeness, account-safety proof, durable media/video preservation,
CAPTCHA/slider solving authorization, Cleaning, ECR, Judgment, buyer proof, or
commercial-readiness evidence.
