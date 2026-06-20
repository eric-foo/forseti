# Data Capture Spine Reddit Graph Frontier Lane Architecture v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture contract
scope: Defines the accepted bounded Reddit Graph Frontier Lane as an agent-mediated frontier-selection and graph-receipt lane downstream of Reddit Candidate URL Intake and upstream of any later bounded intake run.
use_when:
  - Deciding whether Reddit candidate rows may be chained through graph/frontier scouting.
  - Checking what a Graph Frontier Register may persist.
  - Preventing bounded Reddit exploration from becoming same-run traversal, broad crawling, Source Capture, Data Capture, or production crawl infrastructure.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md
  - docs/workflows/reddit_candidate_intake_to_projection_lane_handoff_v0.md
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
  - docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md
  - orca/product/spines/capture/core/contracts/source_access_boundary/data_capture_source_access_boundary_decision_v0.md
stale_if:
  - Candidate URL Intake changes row outputs, provenance fields, same-run traversal rules, promotion gates, or Reddit source-surface policy.
  - Reddit source-access authority changes robots.txt handling, old Reddit posture, broad-crawler authorization, API/commercial requirements, or anti-blocking hard stops.
  - A later accepted graph/frontier, semantic projection, scheduler, storage, or production-runtime contract supersedes this lane.
```

## Status

Status: `OWNER_DIRECTION_ACCEPTED`.

Owner accepts the architecture direction for an agent-mediated **Reddit Graph
Frontier Lane**. The lane may use an agent to choose the next frontier node and
prepare the next bounded run. Every expansion hop must still be separately
bounded, receipted, and stopped.

This lane is not automatic capture, not live Reddit execution, not broad
crawling, and not production crawl infrastructure. Bounded live first-contact
fetch belongs to Reddit Candidate URL Intake, not to the Graph Frontier Register.

Recommended durable record shape: **Graph Frontier Register**.

## Implementation Status

Local no-live foundation exists under:

`orca-harness/capture_spine/reddit_graph_frontier/`

It can build a Graph Frontier Register from existing Candidate URL Intake output,
record frontier decisions, prepare a next bounded run envelope with
`execution_authorized: false`, and write JSON/receipt artifacts. It does not
fetch Reddit, invoke Source Capture Armory, emit Source Capture Packets (CapturePacket), persist
raw HTML, run a scheduler, create storage, or operate as production runtime.
The separate live first-contact runner is
`orca-harness/runners/run_reddit_candidate_intake_live.py`.

Operator-facing "crawling graph" support exists at
`orca-harness/runners/run_reddit_graph_frontier_register.py`. The runner reads a
Candidate URL Intake output artifact, writes a Graph Frontier Register, and can
prepare a non-executing next-run envelope from an operator/frontier-selected
candidate node. It does not fetch Reddit itself.

## Source Context Status

`SOURCE_CONTEXT_READY` for docs-only architecture consolidation. The external
Reddit policy surfaces below were checked on 2026-06-08 for current routing
awareness, but this artifact does not claim legal sufficiency, rights clearance,
API approval, live Reddit access, or commercial permission.

Source basis:

- `docs/workflows/reddit_candidate_intake_to_projection_lane_handoff_v0.md`
- `docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md`
- `docs/workflows/reddit_candidate_intake_old_reddit_search_surface_handling_v0.md`
- `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md`
- `docs/product/data_capture_source_access_boundary_decision_v0.md`
- `https://www.reddit.com/robots.txt`
- `https://redditinc.com/policies/data-api-terms`
- `https://support.reddithelp.com/hc/en-us/articles/26410290525844-Public-Content-Policy`

External policy observations checked on 2026-06-08:

- Reddit robots.txt disallows multiple automated surfaces, including `.json`,
  search, API, subreddit listing, user-after, comments sort, media, gallery, and
  related service endpoints for generic user agents. The Graph Frontier Lane
  must record the robots/source-policy posture for each bounded run and must not
  treat robots.txt as irrelevant just because the run is small.
- Reddit Data API Terms require Data API use to comply with Reddit's terms and
  state that commercial, over-limit, or non-expressly-permitted uses require a
  separate agreement.
- Reddit Public Content Policy is a policy surface about public content and
  related data in the AI era; it is a required awareness surface, not a license
  for Orca to store or capture bodies/comments/profiles in this lane.

## Cynefin Routing Result

Smallest complete outcome: ratify a separate bounded Graph Frontier Lane and
Graph Frontier Register without implementation.

Regime: complicated with a complex edge around source-policy compliance and
automatic expansion risk.

Why: Orca already has candidate-intake and source-access boundaries, but
agent-selected frontier hops could accidentally collapse into a crawler graph
unless every hop remains a separate bounded run.

Decomposition: layer-based with hard stop gates.

Current bottleneck: preserving the difference between graph memory/frontier
selection and same-run traversal.

Riskiest assumption: an agent choosing the next seed will be mistaken for an
autonomous crawler loop.

Stop or pivot condition: if the lane needs persistent queues, timers, dashboards,
databases, raw HTML, body/comment/profile capture, or direct capture handoff,
this artifact is the wrong authority and a separate implementation/runtime
decision is required.

Allowed next move: docs-only map/submap updates and later implementation scoping
for the smallest bounded register/receipt foundation.

Disallowed next move: Graph Frontier-owned live Reddit fetch, production crawler
engine, scheduler, dashboard, storage service, Source Capture Packet generation,
or Data Capture handoff.

## Lane Ownership

Owner lane: **Reddit Graph Frontier Lane**, under Capture Spine / Candidate URL
Intake adjacency.

It is downstream of Reddit Candidate URL Intake and upstream of the next bounded
Candidate URL Intake run. It is not Source Capture Armory and does not own Data
Capture promotion.

Related lanes:

- Candidate URL Intake emits structural candidate rows and provenance only.
- Semantic Projection / frontier agent may choose the next candidate seed from
  graph context.
- The next bounded intake run executes separately with a new `run_id`.
- Source Capture Armory may later consume promoted URLs, but only after a
  separate promotion gate outside this lane.

## Core Loop

1. Candidate URL Intake emits structural candidate rows and provenance only.
2. Reddit Graph Frontier records discovered nodes, edges, prior pointers, source
   surfaces, caps, stop reasons, and non-claims.
3. Semantic Projection / frontier agent chooses the next candidate seed from
   graph context.
4. A fresh bounded run executes with a new `run_id`, declared surface, caps,
   exclusions, access mode, and stop condition.
5. The result updates the Graph Frontier Register so future runs do not waste
   passes rediscovering the same nodes.

## Graph Frontier Register

The register may persist only planning and provenance structure.

Allowed graph node types (discovered sources and the run that found them):

- `subreddit_candidate`
- `thread_url_candidate`
- `outbound_url_candidate`
- `run`

Frontier decisions and stop events are register vocabulary, not graph nodes: a
frontier decision is a separate `frontier_decisions[]` record (carrying
`frontier_selection_reason` / `frontier_selection_actor` /
`frontier_selection_timestamp`), and a stop is carried as the `stop_reason`
field on nodes/edges (and, when surfaced, as a register stop event). They are
not `FrontierNode` instances because a decision or stop has no
discovered-source shape (no URL, surface, or caps of its own).

Allowed edge types:

- `discovered_from_run`
- `found_on_surface`
- `crosspost_relation`
- `related_subreddit_relation`
- `recommendation_relation`
- `more_like_this_relation`
- `outbound_link_relation`
- `selected_as_next_frontier`
- `rejected_for_frontier`
- `already_seen`
- `blocked_or_empty`

Required node/edge fields:

- `register_id`
- `run_id`
- `prior_pointer_or_none`
- `source_surface`
- `source_url_or_locator`
- `query_or_seed`
- `sort_order_or_none`
- `time_window_or_none`
- `timestamp`
- `method_category`
- `access_mode`
- `caps_applied`
- `exclusions`
- `stop_reason`
- `non_claims`

Optional fields:

- `visible_subscriber_count_or_none`
- `visible_active_user_count_or_none`
- `visible_volume_signal_absent_reason_or_none`
- `frontier_selection_reason`
- `frontier_selection_actor`
- `frontier_selection_timestamp`

## Semantic Boundary

Semantic scoring means relevance or quality judgment based on meaning:
ranking, thresholding, suppressing, prioritizing, or selecting candidates.

Semantic scoring is allowed only in the semantic/frontier layer. It is forbidden
inside Candidate URL Intake.

Allowed semantic/frontier acts:

- choose the next candidate seed from already emitted candidate rows;
- record a planning reason for selecting or rejecting a frontier node;
- suppress a candidate from the next hop to avoid irrelevant or duplicate work;
- prioritize bounded next-run preparation.

Forbidden semantic/frontier acts:

- source-quality scoring;
- Data Capture promotion;
- fixture admission;
- body/comment/profile capture;
- same-run traversal;
- claiming coverage, sufficiency, validation, or readiness.

## Hop Gate

Every expansion hop must create a fresh bounded run envelope before execution:

- new `run_id`;
- declared topic/theme/query or seed;
- declared candidate surface;
- declared access mode;
- caps for subreddits, threads, pages/result surfaces, depth, and total frontier
  candidates considered;
- exclusions;
- source-policy/robots posture receipt;
- stop condition;
- non-commercial posture;
- prior register pointer.

The prior stop reason must remain visible. A blocked, empty, capped, or
duplicate-heavy outcome is valid and must not silently widen the next run.

## Accepted Cuts

- no same-run traversal;
- no automatic capture;
- no semantic scoring inside Candidate URL Intake;
- no source-quality scoring;
- no Reddit body/comment/profile capture;
- no raw HTML persistence;
- no Source Capture Packet output;
- no Data Capture handoff;
- no scheduler, dashboard, storage, or production runtime in this lane.

Scheduler, dashboard, storage, and runtime mean standing infrastructure, not
bounded operator/agent runs. A scheduler would auto-run on a timer; a dashboard
would manage a persistent crawl queue or UI; storage means database/corpus
persistence beyond graph receipts; runtime means a long-lived service. These
are deferred because they would turn bounded exploration into operating
infrastructure.

## Success Signals

The lane is in-bounds only when:

- every hop has a new `run_id`;
- every hop has a declared seed/surface, caps, exclusions, access mode, and stop
  condition;
- every hop records a source-policy/robots posture receipt;
- the Graph Frontier Register contains only nodes, edges, pointers, provenance,
  stop reasons, and non-claims;
- semantic/frontier selection happens outside Candidate URL Intake;
- prior stop reasons remain visible;
- duplicate/seen nodes prevent wasted passes without authorizing broader crawl;
- blocked and empty outcomes remain valid terminal results;
- no body/comment/profile text or raw HTML is persisted;
- no Source Capture Packet, Data Capture handoff, source-quality score, fixture
  admission, ECR, Cleaning, Judgment, commercial-use claim, validation claim, or
  readiness claim is emitted.

## Next Authorized Step

Allowed next step: operator review of the Graph Frontier Python foundation or a
fresh bounded Candidate URL Intake run prepared from the register.

Still not authorized:

- Graph Frontier-owned live Reddit fetch;
- automatic expansion execution;
- Source Capture Armory runner dispatch;
- Source Capture Packet generation;
- production scheduler/dashboard/storage/runtime;
- commercial Reddit use;
- Data Capture handoff.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Orca now accepts a separate agent-mediated Reddit Graph Frontier Lane with a
    Graph Frontier Register: it may select the next frontier node and prepare
    the next bounded run, but every hop requires a new bounded run envelope,
    receipt, stop reason, and source-policy posture, while Candidate URL Intake
    remains structural rows/provenance only.
  trigger: architecture_doctrine
  related_triggers:
    - workflow_authority
    - output_authority
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/product/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md
    - docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md
    - docs/workflows/reddit_candidate_intake_to_projection_lane_handoff_v0.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
    - docs/workflows/orca_repo_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/source-of-truth.md
    - docs/workflows/reddit_candidate_intake_old_reddit_search_surface_handling_v0.md
    - docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md
    - docs/product/data_capture_source_access_boundary_decision_v0.md
  intentionally_not_updated:
    - path: orca/product/spines/capture/core/source_capture_toolbox/README.md
      reason: >
        The Graph Frontier Lane is not Source Capture Armory and does not emit
        Source Capture Packets; adding it to the Armory README would blur
        ownership.
    - path: orca-harness/docs/source_capture_agent_runbook.md
      reason: >
        No runner behavior changed. Implementation scoping may later define a
        register/receipt foundation, but this artifact does not authorize or
        document a runnable tool.
    - path: docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md
      reason: >
        Source-access build authorization is not amended. Live Reddit access,
        broad crawler/spider builds, storage, scheduler, dashboard, production
        runtime, and commercial use remain separately gated.
  stale_language_search: >
    rg -n "crawler-graph|crawler graph|Graph Frontier|frontier|candidate_graph_ledger|same-run traversal|automatic capture|Source Capture Packet|Data Capture handoff|scheduler|dashboard|storage|production runtime"
    docs/workflows/orca_repo_map_v0.md
    docs/workflows/data_capture_spine_consolidation_map_v0.md
    docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md
    docs/product/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md
    docs/workflows/reddit_candidate_intake_to_projection_lane_handoff_v0.md
  non_claims:
    - not validation
    - not readiness
    - not legal sufficiency
    - not live Reddit authorization
    - not implementation authorization
    - not broad crawling authorization
    - not Source Capture
    - not Data Capture
    - not commercial permission
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Reddit Graph Frontier Register node types are the discovered-source and run
    types only (subreddit_candidate, thread_url_candidate,
    outbound_url_candidate, run). Frontier decisions are a separate
    frontier_decisions[] register structure and a stop is a stop_reason
    field/event -- they are not FrontierNode instances.
  trigger: architecture_doctrine
  controlling_sources_updated:
    - docs/product/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md
  downstream_surfaces_checked:
    - orca-harness/capture_spine/reddit_graph_frontier/models.py
    - orca-harness/capture_spine/reddit_graph_frontier/register.py
    - orca-harness/capture_spine/reddit_graph_frontier/validation.py
    - docs/workflows/reddit_candidate_intake_to_projection_lane_handoff_v0.md
  intentionally_not_updated:
    - path: docs/workflows/reddit_candidate_intake_to_projection_lane_handoff_v0.md
      reason: >
        It describes the register as recording nodes/edges/decisions without
        enumerating FrontierNode types, so the node-type reconciliation requires
        no change there.
  stale_language_search: >
    rg -n "frontier_decision|stop_event" on the contract and
    orca-harness/capture_spine/reddit_graph_frontier
  stale_language_search_result: >
    Run after this patch. The only contract hit is the new clarifying note that a
    frontier decision is a separate frontier_decisions[] record. Code hits are
    the FrontierDecision structure and frontier_decisions handling in
    register.py / validation.py / writer.py plus the FrontierNodeType clarifying
    comment; FrontierNodeType.FRONTIER_DECISION and .STOP_EVENT no longer exist
    and are referenced nowhere. Focused frontier tests: 11 passed.
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not live Reddit authorization
    - not Source Capture
    - not Data Capture
```

## Non-Claims

This artifact is not validation, readiness, legal sufficiency, rights clearance,
live Reddit access, implementation execution, broad crawling authorization,
automatic capture, Source Capture, Source Capture Packet output, Data Capture
handoff, commercial permission, scheduler authorization, dashboard
authorization, storage authorization, production-runtime authorization, ECR,
Cleaning, Judgment, fixture admission, source-quality scoring, commit
authorization, push authorization, or PR authorization.
