# Capture Source Family: Reddit

```yaml
retrieval_header_version: 1
artifact_role: Capture source-family lane index
scope: >
  Cold-start lane index for bounded Reddit candidate intake, graph/frontier
  planning, exact-thread capture, consolidation, and ECR consumption seams.
use_when:
  - Starting or reviewing bounded Reddit capture or candidate-intake work.
  - Routing a "capture Reddit" request from the Source Capture Playbook into source-specific contracts and runners.
  - Checking where Reddit discovery/select/capture/read responsibilities split.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/social_media/reddit/reddit_subreddit_registry_spec_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/reddit/reddit_radar_grid_capture_maintenance_design_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/reddit_capture_operator_playbook_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md
  - docs/workflows/reddit_capture_to_ecr_consumption_probe_finding_v0.md
  - forseti/product/spines/scanning/source_families/reddit/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md
  - forseti/product/spines/data_lake/README.md
stale_if:
  - Old Reddit HTML, Reddit Direct HTTP batch, warm same-context JSON, CloakBrowser/proxy posture, or commercial Reddit policy changes.
  - Candidate URL Intake or Reddit Graph Frontier contracts change promotion, traversal, or output boundaries.
  - Reddit consolidation/projection/ECR consumption behavior changes.
```

## Stage Split

Reddit has separate stage owners. Do not collapse them into one crawler.

| Stage | Owner / route | Runner / code | Output boundary |
| --- | --- | --- | --- |
| Discover | Candidate URL Intake contracts and old Reddit search/listing handling docs | `run_reddit_candidate_intake_live.py` | Candidate subreddit/thread/outbound URL rows only; no bodies and no Source Capture Packet. |
| Select | Reddit Graph Frontier lane | `run_reddit_graph_frontier_register.py` | Frontier/register receipts and fresh bounded run envelopes; no same-run traversal. |
| Capture | `reddit_capture_operator_playbook_v0.md` | `run_reddit_old_http_batch.py`; `run_reddit_consolidation.py`; `run_reddit_batch_quality_summary.py` | Exact old Reddit thread packets plus derived consolidation outputs. |
| Fallback | Source Capture Playbook archive route and Reddit operator playbook | `run_source_capture_archive_packet.py`; one-URL CloakBrowser runner when explicitly needed | Same-thread archive/capture only; no discovery, profile capture, or broad crawl. |
| ECR / downstream | `docs/workflows/reddit_capture_to_ecr_consumption_probe_finding_v0.md` plus ECR authority | `orca-harness/ecr/deriver.py`; Reddit consolidation/projection helpers | ECR consumes packets source-agnostically; no automatic cleared posture without a Decision Frame/cutoff posture. |

## Known-Venue Preflight

Before opening discovery, graph-frontier, or capture work on a subreddit,
check `reddit_subreddit_registry_v0.json` (contract:
`reddit_subreddit_registry_spec_v0.md`, same folder): known rows are
refreshed, not re-explored, and dated size observations append there. The
registry is routing/dedupe state only — it authorizes nothing and scores
nothing.

## Current Operator Default

For exact old Reddit thread URLs, use old Reddit Direct HTTP first when current
old Reddit HTML is the capture target and the runner accepts the URL. Use
CloakBrowser only for one supplied URL when browser-visible anti-blocking
capture is explicitly needed or Direct HTTP is unsuitable/blocked.

The source family string used by the old HTTP batch runner is `reddit_thread`
with source surface `old_reddit_direct_http`.

## Radar Cadence and Access Posture

Registry-scoped radar grid capture is an accepted direction
(owner-directed 2026-07-16; design:
`reddit_radar_grid_capture_maintenance_design_v0.md`): roughly daily grid
passes per tracked subreddit, stepped to 2–4x daily for trending subs,
following the TikTok grid→deep-dive pattern. Access is dual-track: bounded
public capture under the measured-risk ToS-gated posture AND a sanctioned
commercial/enterprise API or data-licensing path pursued in parallel;
commercial-grade product use lands on the sanctioned path. Every pass
still records its per-run robots/source-policy posture receipt, and the
lane must be built before anything runs.

## Hard Stops

- No broad subreddit crawling beyond registry-tracked grid passes and
  their selected deep dives; no source-discovery expansion outside bounded
  runs; no user/profile capture; no dashboards.
- Candidate URL Intake rows do not auto-promote into Capture units.
- Cold anonymous `.json` is not the default target; warm same-context JSON is a
  future/specialized path only after exact old Reddit HTML is visible.

## Non-Claims

Not validation, readiness, source completeness, fixture admission, commercial
Reddit authority, monitoring authorization, ECR/Judgment proof, Cleaning
authority, buyer proof, or legal advice.
