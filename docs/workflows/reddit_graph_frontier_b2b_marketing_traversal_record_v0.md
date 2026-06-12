# Reddit Graph Frontier B2B-Marketing Traversal Record v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow record
scope: >
  Durable record of the Reddit Graph Frontier traversal for the B2B-marketing
  subreddit-scouting line: realized hop lineage, the current formal
  frontier-selection decision, the non-executing next-run envelope, and the
  provisional selection-recording convention. Planning and provenance only.
use_when:
  - Resuming Reddit graph frontier selection on the B2B-marketing line.
  - Checking which frontier hops are already run versus pending.
  - Recording the next frontier-selection decision under the same convention.
authority_boundary: retrieval_only
open_next:
  - docs/product/data_capture_spine/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md
  - docs/workflows/reddit_candidate_intake_to_projection_lane_handoff_v0.md
  - docs/workflows/reddit_candidate_intake_subreddit_projection_seo_002_closeout_v0.md
stale_if:
  - The Graph Frontier Register schema or selection convention changes.
  - A later hop supersedes the current frontier edge.
  - The referenced scratch runs are regenerated or admitted as fixtures.
```

## Status

Status: `FRONTIER_SELECTION_RECORDED_NON_EXECUTING`.

This is a planning/provenance record. It selects the next frontier seed and
records a non-executing next-run envelope. It does not authorize live Reddit
access, capture, promotion, fixture admission, or same-run traversal. The
underlying Candidate URL Intake JSON artifacts are gitignored scratch under
`orca-harness/_test_runs/` and are referenced by pointer only.

## Decision Frame

- Criterion: topical relevance to **b2b marketing adjacent subreddit scouting**
  (the theme used across the realized runs), judged at candidate name/context
  level only.
- Scope: planning-only selection from an existing Candidate URL Intake output;
  no live access; judgment recorded outside Candidate URL Intake; no promotion.
- Purpose: this B2B-marketing line is a **test vehicle for the frontier arm**
  (traverse -> select -> record -> non-executing envelope). The owner is
  subreddit-agnostic; the specific subreddits are not a content goal.
- Owner of the selection call: Chief Architect / user. Owner confirmed the
  `r/marketing` selection below on 2026-06-08.

## Realized Traversal (lineage)

The runs below were executed as bounded live Candidate URL Intake runs on
2026-06-07 and persist only as gitignored scratch. They are recorded here as
lineage, not re-queued.

| Hop | Seed | Run id (scratch, `_test_runs/`) | Time (UTC) | Produced candidates |
|---|---|---|---|---|
| 0 | SEO | `reddit_candidate_subreddit_discovery_seo_002` / `reddit_live_candidate_intake_seo_related_001` | 20:04 | webmarketing, socialmedia, PPC, analytics |
| 1 | webmarketing | `reddit_live_candidate_intake_webmarketing_related_001` | 20:18 | marketing, socialmedia, advertising, digital_marketing, analytics, DigitalMarketing, AskMarketing |

Also run from hop-0 candidates: `reddit_live_candidate_intake_ppc_related_001`,
`reddit_live_candidate_intake_socialmedia_related_001`. Hop-0 candidate
`analytics` was not run. The `SEO -> webmarketing` selection (hop 1) was realized.

## Current Frontier Selection (hop 2)

- Register built from: `reddit_live_candidate_intake_webmarketing_related_001`
  (the live frontier edge).
- Selected next seed: **`r/marketing`** (un-run).
- Selection reason (4-part seam):
  - **Candidates considered:** marketing, advertising, digital_marketing,
    analytics, DigitalMarketing, AskMarketing (socialmedia already explored).
  - **Chosen:** `marketing` — most central, highest-reach general-marketing hub,
    most likely to host B2B-marketing practitioner threads.
  - **Deciding signal:** topical centrality to the B2B-marketing theme among the
    related-subreddit rows.
  - **Why-not:** advertising/analytics (narrower specialties); AskMarketing (Q&A
    format); DigitalMarketing/digital_marketing (channel-specific variants).
- **Surface-bias observation (corrected — see Arm Evaluation Note):**
  webmarketing's children broaden toward *general* marketing. An external web
  check (2026-06-08) shows the B2B space is **not** exhausted; recognized
  B2B-specific communities exist that this sidebar surface does not reach.

Realized register + envelope (scratch, verified, `execution_authorized: false`):
`orca-harness/_test_runs/reddit_graph_frontier_webmarketing_001/`
(`reddit_graph_frontier_register.json`, `reddit_graph_frontier_next_run_envelope.json`).

## Non-Executing Next-Run Envelope

For the would-be next bounded Candidate URL Intake run on `r/marketing`. Intent
only; nothing is authorized to execute.

```yaml
next_run_id: reddit_live_candidate_intake_marketing_related_001
selected_seed: marketing
declared_topic_theme_or_query: b2b marketing adjacent subreddit scouting
candidate_surface_allowlist: [related_subreddit]
caps:
  max_subreddits: 5
  max_threads_per_subreddit: 25
  max_pages_or_result_surfaces: 1
  max_frontier_hops: 1
exclusions: [no_same_run_traversal, no_body_comment_profile_capture, no_user_profiles]
access_mode: live_old_reddit_direct_http_candidate_intake
source_policy_posture: robots_policy_recorded_before_any_live_access
stop_condition: caps_reached
execution_authorized: false
```

## Arm Evaluation Note

This line tests the frontier arm, not B2B content. One arm finding from a
2026-06-08 external web check (meta-research to validate an exhaustion claim --
**not** Reddit capture, candidate intake, or live source access):

- The related-subreddit **sidebar** surface drifts toward general-marketing hubs
  (marketing, advertising, digital_marketing) and does **not** surface
  B2B-specific practitioner communities. Recognized B2B communities such as
  r/sales, r/leadgeneration, r/demandgeneration, r/SaaS, r/startups,
  r/smallbusiness, and r/Entrepreneur were not reached by sidebar hops from SEO
  or webmarketing.
- An earlier "near-exhausted for B2B" reading was therefore overstated: the B2B
  **space** is not exhausted; the sidebar **discovery surface** under-reaches
  specialized communities that do not cross-link via sidebars.
- Arm implication: related-subreddit-sidebar traversal has a
  topical-drift-to-general bias. Reaching specialized communities would need a
  different discovery surface (topic search or direct seeding), not more sidebar
  hops.

External sources (non-Reddit-capture): linkeddit.com best-subreddits-b2b-lead-
generation-2026; infrasity.com reddit-b2b-marketing-strategy; redreach.ai
10-most-effective-subreddits-for-b2b-lead-generation.

## Discovery-Surface Design (arm)

The arm reaches candidate subreddits through discovery surfaces. The realized
runs used only the related-subreddit sidebar; the Arm Evaluation Note shows that
surface drifts to general hubs and under-reaches specialized verticals. The
intended arm design combines three complementary surfaces, sequenced by lock-in:

| Surface | Finds subs by | Recall bias | Lock-in |
|---|---|---|---|
| Related-subreddit sidebar (realized) | adjacency cross-links | drifts to general hubs | in this lane |
| Reddit search listing | Reddit's own keyword index | name/topic match; reaches non-sidebar-linked subs | in this lane: a declared-and-capped candidate surface (`CandidateSurface.REDDIT_SEARCH_LISTING`) |
| External web / SERP | external authority and recency | listicle-grade verticals neither surface above reaches | OUT of this lane: different source family; SERP/discovery builds deferred by the crawler contract |

The surfaces are complementary, not redundant: each has a different recall bias,
so combining them improves reach for specialized communities more than any one
alone. This is arm design, not a content goal; the owner remains
subreddit-agnostic.

### Resolved -- keep sidebar traversal (Q1)

The related-subreddit sidebar surface is kept as a secondary adjacency surface,
not culled. It is complementary to search (adjacency bias vs vertical-relevance
bias) and adds reach rather than duplicating it. Owner-confirmed 2026-06-08.

### Resolved -- external web / SERP placement (option 1)

Switching on Reddit search is an in-lane config choice (declare the surface and
cap it). Binding **external** web search is a separate, higher-lock-in decision
that is NOT a toggle inside Reddit Candidate URL Intake:

- Reddit Candidate URL Intake is Reddit-source-family only; web-search results
  are a different source family (outbound / separate-family intake), not Reddit
  candidate rows.
- The crawler architecture contract defers SERP/discovery-API builds.

The question was: **where do web-discovered subreddits live?** Owner-chosen
2026-06-08: **option 1 -- a sibling web-discovery surface** that emits subreddit
candidates into the same Graph Frontier Register, kept distinct from
Reddit-source intake. This keeps the source-family boundary clean (web finds are
not laundered into Reddit candidate rows) at the cost of a new surface.

Not chosen: (2) outbound-URL rows inside the existing lane, promoted separately;
(3) defer to sidebar + Reddit search only.

This resolution sets direction only. It does not authorize a build: the sibling
surface still requires the deferred SERP/discovery-API gate and a concrete
scoped design before implementation. Reddit search remains independently
available as an in-lane surface.

## Selection-Recording Convention (provisional)

Each frontier selection records the 4-part seam above: (1) candidates considered,
(2) the one chosen, (3) the deciding signal, (4) why-not for the rest. This is a
provisional, lane-local convention — not yet doctrine. It exists so that after a
few hops a reusable selection rule can be induced from the recorded decisions (or
this convention promoted into the Graph Frontier contract). It elaborates, and
does not replace, the contract's requirement to record a planning reason for each
frontier node.

## Non-Claims

Not validation, readiness, source completeness, canonical evidence, fixture
admission, live Reddit authorization, capture, Source Capture Packet output, Data
Capture handoff, ECR, Cleaning, Judgment, promotion, or commercial permission.
The referenced scratch runs are not admitted as fixtures by this record.
