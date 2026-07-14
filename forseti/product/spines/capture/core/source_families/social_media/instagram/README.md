# Capture Source Family: Instagram

```yaml
retrieval_header_version: 1
artifact_role: Forseti Capture source-family README
scope: >
  Directory entrypoint for Instagram artifacts under the Capture core
  social_media source-family grouping.
use_when:
  - Starting Instagram capture source-family work.
  - Checking the Capture-vs-Scanning phase placement for Instagram artifacts.
  - Finding the first Instagram capture contracts, probes, or architecture notes to open.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/README.md
  - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_capture_findings_consolidated_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_daily_heartbeat_operating_policy_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/instagram/forseti_creator_monitoring_policy_architecture_v0.md
  - forseti/product/spines/data_lake/README.md
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
```

This directory is the current Capture home for Instagram source-family
artifacts, grouped under `social_media/` because Instagram is a social-media
source family, not a peer Capture spine.

Phase sibling status: no accepted
`forseti/product/spines/scanning/source_families/instagram/` directory exists in
this worktree. If a Scanning Instagram source family is later created, add the
cross-pointer here and in the Scanning family entrypoint.

## Capture-To-Lake Route Map

| Layer | Current home | What to confirm |
| --- | --- | --- |
| Access / method | `ig_capture_findings_consolidated_v0.md`, `ig_wind_caller_capture_feasibility_recon_v0.md`, `ig_reel_viewcount_capture_feasibility_recon_v0.md`, `ig_creator_discovery_suggested_accounts_recon_v0.md` | Public/logged-out versus entitled-session posture, per-route residuals, and route-specific source surfaces. |
| Daily heartbeat policy and control | `ig_daily_heartbeat_operating_policy_v0.md`; `forseti-harness/source_capture/social_heartbeat_run_control.py`; `run_source_capture_ig_daily_heartbeat.py`, `_control.py`, and `_operator.py` | Steady daily registered-creator grid heartbeat. Instagram supplies roster/capture policy while shared control owns plan, partition, lease, attempt, strict receipt, and summaries; excludes onboarding, Silver, and a standing scheduler. |
| Grid / creator capture | `forseti-harness/runners/run_source_capture_ig_reels_grid_packet.py`; `run_source_capture_ig_calls_packet.py`; `run_source_capture_ig_calls_batch.py` | Packet writes over bounded public creator/reels surfaces; no source discovery widening unless the owning discovery lane authorizes it. |
| Deep capture / transcript | `forseti-harness/runners/run_source_capture_ig_reels_deep_capture.py`; `run_source_capture_ig_reels_creator_deep_capture.py`; `forseti-harness/source_capture/ig_reels_deep_capture.py` | One-render deep capture for comments plus transient media handle ASR; no durable media/video preservation claim unless separately proven. |
| Projection / lake | `forseti-harness/source_capture/ig_projection.py`, `ig_reels_grid_projection.py`, `ig_reels_deep_capture_lake.py`; Data Lake authority docs | Source-surface-preserving projection and lake writes route through existing helpers; lake semantics stay Data Lake-owned. |
| Audience post-text Cleaning seam | `forseti-harness/source_capture/audience_post_packet.py`; `forseti-harness/cleaning/audience_post_input.py`; `forseti-harness/cleaning/audience_extractor.py` | Post-text packets use the platform as `source_family` and `instagram_post_text` as the source surface; the deterministic adapter feeds Pass-1 audience extraction and is not a fake top-level source family. |
| Product extraction / Cleaning | `ig_reels_transcript_product_extraction_spec_v0.md`; `run_ig_reels_product_extract.py`; `run_ig_reels_operator_product_extract.py` | Product mention extraction is downstream Cleaning/Silver/operator-lane work, not Capture authority. |

## Non-Claims

This entrypoint is not live capture authorization, validation, readiness,
source completeness, durable media/video preservation proof, account-safety
proof, Cleaning authority, Judgment, buyer proof, or commercial readiness.
