# Reddit Candidate Intake To Projection Lane Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow handoff
scope: >
  Summarizes completed bounded Reddit Candidate URL Intake work and defines the
  handoff boundary for semantic projection and chain subreddit scouting.
use_when:
  - A separate semantic projection lane needs to consume Reddit Candidate URL
    Intake outputs.
  - Planning chain subreddit scouting without weakening the no-same-run-traversal
    intake contract.
  - Checking whether candidate-subreddit relevance belongs in intake or a later
    layer.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md
  - forseti/product/spines/scanning/source_families/reddit/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md
  - docs/workflows/reddit_candidate_intake_old_reddit_search_surface_handling_v0.md
  - docs/workflows/reddit_candidate_intake_subreddit_projection_b2b_001_closeout_v0.md
  - docs/workflows/reddit_candidate_intake_subreddit_projection_seo_002_closeout_v0.md
stale_if:
  - Candidate URL Intake row schema changes.
  - Semantic projection gets its own durable contract.
  - Chain subreddit scouting gains implementation beyond bounded run receipts.
  - The Reddit Graph Frontier Lane changes hop gates, register fields, non-claims, or implementation-scoping boundary.
```

## Status

Status: `INTAKE_TO_PROJECTION_HANDOFF_READY`.

This handoff does not authorize semantic scoring inside Candidate URL Intake. It
records what intake accomplished and what the next lane may safely consume.

Owner direction update: the separate agent-mediated Reddit Graph Frontier Lane
is now accepted as the target architecture direction. It remains outside
Candidate URL Intake, uses a Graph Frontier Register rather than a generic
ledger, and may choose the next frontier node only by preparing a fresh bounded
run with a new `run_id`, caps, exclusions, access mode, source-policy posture,
and stop condition. This handoff does not authorize live Reddit access or
implementation execution.

## What Intake Now Does

The Reddit Candidate URL Intake lane now supports bounded old Reddit structural
projection into planning-only candidate rows:

- thread URL rows from old Reddit listing/search title anchors;
- seed subreddit candidate rows;
- related subreddit candidate rows from declared related/recommendation-style
  containers;
- related subreddit candidate rows from declared old Reddit sidebar markdown
  links;
- optional visible subscriber/active-user fields only when visibly present on
  the declared surface;
- run envelope, caps, coverage claim, provenance, exclusion receipt, and visible
  stop reason.

The implementation lives in Python under:

```text
orca-harness/capture_spine/reddit_candidate_intake/
```

Python is the right current home for intake because the behavior is deterministic
projection, validation, row writing, and regression testing. It should remain
small and boring: parse bounded old Reddit HTML into rows, validate forbidden
fields, write receipts, and stop.

## What Intake Does Not Do

Candidate URL Intake does not:

- rank or suppress candidates by semantic relevance;
- score source quality;
- enter discovered subreddits in the same run;
- fetch thread bodies or comments;
- capture user/profile/author data;
- persist raw HTML or parser output into candidate output;
- emit Source Capture Packets;
- invoke Source Capture Armory by default;
- promote rows into capture units;
- hand rows directly to Data Capture.

## Completed Evidence

### B2B Seed Projection

Run:

```text
reddit_candidate_subreddit_discovery_b2b_001
```

Observed output:

```text
candidate_subreddits=1
candidate_threads=0
outbound_urls=0
row=b2bmarketing
visible_volume_signal_absent_reason_or_none=visible_volume_not_present_on_declared_surface
same_run_traversal_authorized=false
```

Meaning: `r/b2bmarketing` is established as a planning-only seed candidate row.
The saved page did not expose a declared related-subreddit surface.

### SEO Sidebar Related Projection

Run:

```text
reddit_candidate_subreddit_discovery_seo_002
```

Observed output:

```text
candidate_subreddits=4
candidate_threads=0
outbound_urls=0
rows=webmarketing,socialmedia,PPC,analytics
source_surface=related_subreddit
same_run_traversal_authorized=false
```

Meaning: `r/SEO` exposes hand-authored old Reddit sidebar markdown links that
can be projected as `related_subreddit` candidate rows when the sidebar markdown
surface is declared and page chrome is excluded.

From the candidate names alone, `/r/webmarketing` appears most directly related
to the current B2B marketing theme. That is a planning observation only. It is
not a Candidate URL Intake score, suppression rule, or promotion.

## Handoff Interface For Semantic Projection

The semantic projection lane may consume:

- `candidate_subreddits[]`;
- `candidate_threads[]`;
- `outbound_urls[]`;
- `run_id`;
- `source_surface`;
- `source_url`;
- `query_or_seed`;
- `timestamp`;
- `method_category`;
- `exclusion_receipt`;
- `caps_applied`;
- `coverage_claim`;
- `stop_reason`;
- `visible_subscriber_count_or_none`;
- `visible_active_user_count_or_none`;
- `visible_volume_signal_absent_reason_or_none`;
- intake closeout notes that explicitly label planning observations.

The semantic projection lane must not treat intake rows as:

- capture units;
- Data Capture input;
- Source Capture Packets;
- source-quality scores;
- proof of relevance;
- proof of subreddit volume;
- authorization for same-run traversal.

## Chain Subreddit Scouting Model

Chain subreddit scouting is allowed only as a sequence of bounded runs. It is not
same-run traversal.

Allowed chain shape:

```yaml
chain_scouting:
  chain_id: reddit_b2b_subreddit_chain_001
  step_n:
    input:
      prior_candidate_row_pointer:
      projection_selection_reason:
      declared_seed_subreddit:
      declared_topic_theme_query:
      candidate_surface_allowlist:
      caps:
      exclusions:
    execution:
      new_run_id:
      source_surface:
      method_category:
      access_mode:
    output:
      candidate_rows_only: true
      stop_reason:
      coverage_claim:
      no_same_run_traversal: true
```

Each hop requires:

- a prior candidate row pointer or owner-selected seed;
- a declared reason for choosing that seed;
- a new `run_id`;
- fresh caps and exclusions;
- a visible stop reason;
- candidate/provenance-only output.

## Chain Stop Conditions

Stop the chain when any of these occurs:

- max chain depth reached;
- max total candidate subreddits reached;
- candidate pool is exhausted;
- no candidate meets the semantic projection threshold;
- the next hop would require broad search, API discovery, or same-run traversal;
- raw HTML would need to be promoted into durable output;
- the operator decides the current candidate set is enough for planning.

## Reddit Graph Frontier Boundary

The accepted shape is **Reddit Graph Frontier Lane** with a **Graph Frontier
Register**.

The register records discovered nodes, edges, prior pointers, source surfaces,
caps, stop reasons, source-policy posture, and non-claims. It may use semantic
projection or a frontier agent to choose the next candidate seed, but that
choice only prepares a new bounded run. It does not authorize same-run
traversal, automatic capture, live Reddit access, broad crawling, or production
crawl infrastructure.

The Graph Frontier Lane is a sibling/downstream exploration lane that consumes
Candidate URL Intake rows and writes graph/frontier receipts. Candidate URL
Intake remains a structural row/provenance lane and does not become the graph
expansion engine.

## Smallest Complete Chain Scouting Start

For this workstream, the smallest complete next chain step is not another
generic seed run. It is:

```yaml
chain_id: reddit_b2b_subreddit_chain_001
step: 1
prior_source_run_id: reddit_candidate_subreddit_discovery_seo_002
selected_seed_candidate: webmarketing
selection_basis: >
  Planning observation from candidate name and source context: `/r/webmarketing`
  appears most directly related to the current B2B marketing theme among the
  four `r/SEO` sidebar candidates.
required_before_execution:
  - semantic projection lane accepts or records the selection basis
  - new bounded run envelope
  - source surface declaration
  - caps and exclusions
  - access mode declaration
allowed_output:
  - candidate subreddit rows
  - candidate thread URL rows if separately declared
  - provenance
  - stop reason
forbidden_output:
  - semantic score inside intake output
  - same-run traversal
  - Source Capture Packet
  - Data Capture handoff
```

## Coding Recommendation

Use Python for the mechanical intake/scouting harness after the relevant contract
is settled:

- Candidate URL Intake is already Python because it needs deterministic parsing,
  validation, row writing, and tests.
- Chain scouting should be Python if it remains a repeatable harness that reads
  prior candidate outputs, creates the next run envelope, writes chain receipts,
  and enforces depth/cap/stop rules.
- Reddit Graph Frontier implementation may be scoped only as a bounded
  register/receipt foundation after this accepted architecture is source-mapped.
  It must not start with live Reddit access or automatic expansion execution.
- Semantic projection can start as a planning artifact or review lane if it uses
  human/LLM judgment. Only move it into Python when the selection rule becomes
  stable enough to test deterministically.

The hard boundary is that Python chain scouting may orchestrate separate bounded
runs and receipts, but it must not make Candidate URL Intake perform semantic
ranking or same-run traversal.

## Next Authorized Step

Implementation scoping may proceed for the smallest bounded Graph Frontier
Register foundation: read existing candidate-row receipts, write nodes/edges and
frontier decisions, preserve stop reasons, and prepare the next run envelope
without live Reddit access.

Do not build automatic expansion execution, live Reddit access, Source Capture
Armory dispatch, storage, scheduler, dashboard, or production runtime from this
handoff alone.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Orca now accepts a separate agent-mediated Reddit Graph Frontier Lane with a
    Graph Frontier Register, while Candidate URL Intake remains
    row/provenance-only and does not become the graph expansion engine.
  trigger: architecture_doctrine
  related_triggers:
    - workflow_authority
    - output_authority
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/workflows/reddit_candidate_intake_to_projection_lane_handoff_v0.md
    - docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md
    - docs/product/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
    - docs/workflows/orca_repo_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md
    - docs/workflows/reddit_candidate_intake_old_reddit_search_surface_handling_v0.md
    - docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md
  intentionally_not_updated:
    - path: docs/prompts/deep-thinking/reddit_crawler_graph_exploration_architecture_ca_prompt_v0.md
      reason: >
        The prompt remains a historical commissioning artifact. The accepted
        architecture direction now lives in the Graph Frontier architecture
        contract and maps.
    - path: docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md
      reason: >
        Source-access build authorization has not changed in this patch. Live
        Reddit access, broad crawler/spider builds, storage, scheduler,
        dashboard, production runtime, and commercial use remain separately
        gated.
  stale_language_search: >
    rg -n "crawler-graph|crawler graph|Graph Frontier|graph expansion|broad crawling|Candidate URL Intake"
    docs/workflows/reddit_candidate_intake_to_projection_lane_handoff_v0.md
    docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md
    docs/product/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md
    docs/workflows/reddit_candidate_intake_old_reddit_search_surface_handling_v0.md
    docs/prompts/deep-thinking/reddit_crawler_graph_exploration_architecture_ca_prompt_v0.md
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not crawler build authorization
    - not source-access boundary amendment
    - not Source Capture Packet output
    - not Data Capture handoff
    - not live Reddit authorization
```
