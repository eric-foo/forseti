# TikTok Live Probe Hardening PR 553

```yaml
retrieval_header_version: 1
artifact_role: Repo-map recent-change note
scope: Low-conflict context for the TikTok live batch probe runner and hardening route in PR #553.
use_when:
  - Reconstructing why the TikTok source-capture route mentions live probe hardening.
  - Checking PR #553 repo-map context without appending chronology to the main repo-map header.
open_next:
  - docs/workflows/orca_repo_map_v0.md
  - orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md
  - orca-harness/source_capture/tiktok/live_batch_probe.py
  - orca-harness/source_capture/tiktok/batch_packet.py
authority_boundary: retrieval_only
```

PR #553 adds the one-creator TikTok live staging probe runner and then hardens
it so missing video-detail hydration stops the batch as a possible C6
empty/stripped-shell block signal. The batch admission path also preserves the
live probe `url_present_but_redacted` subtitle receipt as admitted
`url_redacted` metadata.

This note is map context only. It does not claim a live run, cross-creator
ceiling proof, account-safety-at-scale proof, subtitle body fetch, product
extraction, Cleaning, ECR, Judgment, or a persisted derived lane.