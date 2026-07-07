# TikTok Creator Discovery Frontier Register v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture contract (scanning source-family adapter)
scope: >
  Defines the bounded TikTok Creator Discovery Frontier Register: how TikTok
  suggested-account, profile-carousel, and creator-adjacent discovery edges are
  recorded as scanning/frontier structure without becoming Creator Registry
  identity proof, follower-graph capture, live traversal, or capture execution.
use_when:
  - Recording TikTok suggested-account creator discovery from an owner-authorized seed profile.
  - Deciding whether a TikTok creator recommendation edge belongs in Creator Registry or scanning frontier memory.
  - Preparing a bounded next creator scan from prior TikTok discovery edges.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/scanning/source_families/tiktok/tiktok_creator_discovery_enforcement_placement_v0.md
  - forseti/product/spines/scanning/README.md
  - forseti/product/spines/scanning/scan_core/forseti_scanning_intelligent_walk_mgt_operating_model_v0.md
  - forseti/product/spines/scanning/source_families/reddit/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md
stale_if:
  - TikTok suggested-account surfaces move behind a different access posture.
  - A dedicated TikTok discovery harness/schema supersedes this review-input register shape.
  - Creator Registry adopts a first-class cross-platform discovery graph with typed weak edges.
```

## Status

Status: `SPEC_PROPOSED_MGT_FRONTIER_ADAPTER`.

This is a Mini God Tier scanning/frontier adapter: it targets most of the useful
creator-discovery graph value while stopping before standing crawler, monitor,
registry, dashboard, database, or runtime infrastructure. It is not validation,
readiness, live access authorization, registry insertion authorization, or
source-access proof.

## Why This Exists

TikTok suggested-account surfaces are useful because they reveal adjacent creator
candidates from the platform's own recommendation context. They are not useful
as identity proof by themselves.

The register lets Forseti remember:

- which creator seed produced which candidate handles;
- which weak platform edge exposed a candidate;
- whether a candidate was already seen, held, blocked, or selected for a later
  bounded scan;
- which source packet backs the observation;
- which next-run envelope would scan a candidate if the owner launches it.

It deliberately does not say that the candidates are the same creator, followers,
friends, endorsed accounts, US-based, on-niche, or capture-ready.

## Edge Vocabulary

An edge is a typed relation between two nodes. The type is the claim boundary.

For this register:

- `discovered_from_run` means the node was observed during one bounded discovery
  run.
- `platform_suggested_account_relation` means TikTok displayed the candidate as
  a suggested/related account from the seed profile, profile carousel, or
  Followers/Following modal Suggested tab.
- `already_seen` means the candidate was already present in this or another
  register and should not be re-added as a fresh candidate.
- `selected_as_next_frontier` means a human/agent selected that node for a later
  bounded scan; it does not authorize execution.
- `rejected_for_frontier` means the node was deliberately not pursued in the
  current planning pass.
- `blocked_or_empty` means the source-visible surface was unavailable, empty, or
  blocked in a way that should remain visible.

Identity edges are out of scope here. Same-creator claims belong in Creator
Registry linkage evidence after source-visible proof and preflight.

## Register Shape

The register mirrors the existing Reddit/LinkedIn Graph Frontier pattern while
using TikTok creator node types:

```yaml
tiktok_creator_discovery_frontier_register:
  schema_version: tiktok_creator_discovery_frontier_register_v0
  register_id:
  source_run_id:
  root_seed:
    platform: tiktok
    handle:
    url:
  provenance:
    source_surface:
    source_packet_id_or_none:
    source_packet_path_or_none:
    parent_grid_packet_id_or_none:
    parent_grid_packet_path_or_none:
    captured_at_utc:
    method_mode:
    access_mode:
    caps_applied:
    stop_reason:
  nodes:
    - node_id:
      node_type: run | tiktok_creator_seed | tiktok_creator_candidate
      platform: tiktok
      handle_or_none:
      display_name_or_none:
      source_url_or_locator:
      run_id:
      source_surface:
      timestamp:
      method_mode:
      access_mode:
      caps_applied:
      exclusions:
      stop_reason:
      registry_preflight_status_or_none:
      platform_capture_status:
      cross_platform_graph_status:
      non_claims:
  edges:
    - edge_id:
      edge_type:
      from_node_id:
      to_node_id:
      run_id:
      source_surface:
      source_packet_id_or_none:
      observed_sections:
      timestamp:
      method_mode:
      stop_reason:
      confidence:
      non_claims:
  frontier_decisions:
    - decision_id:
      selected_node_id:
      projection_decision: promote | hold | reject | already_seen
      frontier_selection_reason:
      frontier_selection_actor:
      frontier_selection_timestamp:
      next_run_id_or_none:
      non_claims:
  next_run_envelopes:
    - schema_version: tiktok_creator_discovery_next_run_envelope_v0
      next_run_id:
      selected_node_id:
      prior_register_pointer:
      declared_seed_or_surface:
      candidate_surface_allowlist:
      caps:
      exclusions:
      method_mode:
      access_mode:
      source_policy_posture:
      stop_condition:
      execution_authorized: false
      non_claims:
  accepted_residuals:
  non_claims:
```

## Receipt-Backed Writing

The preferred code path is the network-free builder under
`forseti-harness/capture_spine/tiktok_creator_discovery_frontier/`. It consumes a
validated `tiktok_creator_discovery_scan_receipt_v0` plus already-observed
suggested-account rows, then emits this register shape. The receipt records caps,
packet/lake pointers, refresh outcome, pagination bound, browser-close posture,
and no follow/open/screenshot actions. It still does not launch TikTok, create a
live runner, prove source truth, authorize next runs, or mutate Creator Registry.

## Count And Completeness Semantics

`suggested_accounts_observed` is receipt/cap context for source-visible suggested
rows in the scan. The emitted candidate nodes are the rows selected for graphing
after any operator filtering, deduping, or bounded under-sampling. A count mismatch
is not itself a validator failure.

Cold agents must not claim the register exhausts all source-visible suggestions
unless the receipt/register explicitly records that all observed rows were
included. When rows were filtered, deduped, not paginated, or otherwise
under-sampled, record an `accepted_residuals` entry such as:
`Candidate nodes are a filtered/deduped subset of suggested_accounts_observed;
not exhaustive.`

If exact completeness becomes product-critical, add an explicit future field or
mode such as `candidate_rows_mode: exhaustive|filtered_subset` before enforcing
count equality in code.

## Cross-Platform Linkage

Cross-platform linkage is allowed as a separate strong-edge layer only after a
candidate's own source-visible evidence supports it:

1. TikTok discovery frontier sees `@candidate` from a weak recommendation edge.
2. A later bounded candidate scan captures that candidate's TikTok profile/grid
   and bio link hub, if source-visible.
3. Link hub, reciprocal links, or official profile references can create
   Creator Registry linkage evidence for the candidate's IG/YT/TikTok accounts.
4. Registry exact-match preflight routes known accounts as updates and unknown
   accounts as candidates.

The discovery frontier can point to registry candidate IDs when known, but it
must not create them by itself.

## MGT Accepted Residuals

| Residual | Why acceptable now | Remaining risk | Upgrade trigger |
| --- | --- | --- | --- |
| No standing TikTok crawler | Keeps the lane bounded and avoids crawler/runtime lock-in. | Some adjacent creators will be missed between owner-launched runs. | Repeated missed high-value creators or sustained multi-operator discovery cadence. |
| No live auto-pagination requirement | Keeps capture posture safe and session-visible. | The register may under-sample a suggested list. | Owner authorizes a bounded pagination probe with explicit caps and source-access posture. |
| Candidate count may differ from observed suggestion count | Allows bounded filtering/deduping without making false completeness claims. | A cold agent could overstate recall if it ignores accepted_residuals. | Exact completeness becomes product-critical and receives an explicit schema mode. |
| No ranking model | Repeated coappearance and manual selection carry enough early value. | Frontier ordering may be inconsistent. | Repeated low-yield scans from poor ordering or enough graph receipts to justify a transparent ranker. |
| No registry mutation | Preserves identity quality and duplicate safety. | Extra preflight step before onboarding. | Registry adopts a typed weak-edge intake lane with deterministic duplicate routing. |
| No full graph database | JSON registers are enough for current owner-launched scans. | Cross-run querying is manual or script-assisted. | Same vertical reaches repeated weekly scans or multi-root snowball management. |

## Enforcement Placement

For code-versus-doctrine placement before further scouting, open `forseti/product/spines/scanning/source_families/tiktok/tiktok_creator_discovery_enforcement_placement_v0.md`. The frontier spec defines the target shape; the enforcement-placement artifact classifies which behaviors need future validators/hooks/runners and which remain resident doctrine for cold agents.

## Hard Stops

- No same-run unbounded traversal.
- No standing crawler, monitor, dashboard, queue, or graph database.
- No follower/following graph claim unless that source-visible relationship was
  separately captured and typed.
- No registry insertion from recommendation edges alone.
- No contact enrichment.
- No private identity inference.
- No screenshots in chat by default.
- No metric zero-fill from discovery/link-hub observations.
- No CAPTCHA solving, proxy/account-rotation plan, forged signatures, or
  platform API replay.

## Non-Claims

Not validation, readiness, capture success, account-safety proof, source-access
authorization, Creator Registry identity proof, follower graph, endorsement
proof, country/region evidence, metric rollup, commercial permission, or
production infrastructure authorization.
