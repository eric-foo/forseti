# Data Capture Spine Reddit Candidate URL Intake Crawler Architecture v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture contract
scope: Defines bounded Reddit Candidate URL Intake as a Capture Spine candidate-intake lane that emits URL candidates and provenance only, before any Source Capture Armory packet capture or Data Capture handoff.
use_when:
  - Deciding where an operator-facing Reddit crawler belongs in Orca.
  - Checking what bounded Reddit candidate URL intake may output before promotion.
  - Preventing Reddit candidate enumeration from becoming broad crawling, Source Capture Armory capture, or unreviewed Data Capture input.
authority_boundary: retrieval_only
open_next:
  - docs/product/data_capture_spine_candidate_url_intake_contract_v0.md
  - docs/product/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md
  - docs/decisions/data_capture_spine_reddit_candidate_url_intake_default_policy_decision_v0.md
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
  - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md
  - docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md
stale_if:
  - The parent Candidate URL Intake contract changes run-envelope, row-schema, cap, stop, promotion, or traversal rules.
  - The Reddit Candidate URL Intake default-policy decision changes default caps, surfaces, outbound policy, monitoring posture, promotion ownership, or implementation-scoping gate.
  - The Reddit Graph Frontier Lane changes hop gates, register fields, same-run traversal boundary, or semantic/frontier ownership.
  - Orca creates or supersedes a Candidate Signal Intake / Corpus Intake contract.
  - The Data Capture obligation contract changes commissioned-capture scope or forbidden outputs.
  - Reddit source-access ordering, selected backend, or broad-crawler build authorization changes.
  - Source Capture Packet lifecycle or Armory runner boundaries move to a new owner.
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Owner direction now permits bounded live Reddit first-contact Candidate
    URL Intake for declared source-surface sourcing when a concrete run
    envelope and explicit live-access authorization are present. This does not
    move sourcing into Source Capture Armory, does not authorize same-run
    traversal, and does not authorize Source Capture Packet output.
  trigger: implementation_boundary
  related_triggers:
    - source_access_boundary
    - workflow_authority
    - lifecycle_boundary
    - output_authority
  controlling_sources_updated:
    - "docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md"
    - "docs/product/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md"
    - "docs/workflows/data_capture_spine_consolidation_map_v0.md"
    - "docs/workflows/orca_repo_map_v0.md"
    - "orca-harness/runners/run_reddit_candidate_intake_live.py"
    - "orca-harness/capture_spine/reddit_candidate_intake/__init__.py"
    - "orca-harness/tests/unit/test_reddit_candidate_intake_live_runner.py"
  downstream_surfaces_checked:
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/decision-routing.md"
    - "docs/product/source_capture_toolbox/reddit_capture_operator_playbook_v0.md"
    - "docs/workflows/data_capture_spine_consolidation_map_v0.md"
    - "docs/workflows/orca_repo_map_v0.md"
  intentionally_not_updated:
    - path: "docs/product/source_capture_toolbox/README.md"
      reason: >
        The live first-contact runner is Candidate URL Intake, not Source
        Capture Armory. Armory remains downstream exact-URL packet capture after
        promotion.
    - path: "orca-harness/docs/source_capture_agent_runbook.md"
      reason: >
        The source-capture runbook remains for Source Capture Packet runners.
        Candidate URL Intake runner closeout belongs to this lane and the repo
        submap route.
  non_claims:
    - "not validation"
    - "not readiness"
    - "not legal sufficiency"
    - "not commercial Reddit authorization"
    - "not broad crawler authorization"
    - "not Source Capture Armory authorization"
    - "not Source Capture Packet output"
    - "not Data Capture handoff"
```

## Status

Status: `TARGET_RECOMMENDED`.

This artifact ratifies the architecture placement and output contract for the
operator-facing bounded Reddit "crawler." The architectural contract name is
**Bounded Reddit Candidate URL Intake**.

This artifact is a Reddit source-family specialization of
`docs/product/data_capture_spine_candidate_url_intake_contract_v0.md`. The parent
contract owns generic Candidate URL Intake row shapes, run envelopes, cap
semantics, promotion gates, and traversal stops. This Reddit artifact owns
Reddit-specific surfaces and field names.

The operator-facing name may remain `crawler`, but durable Orca routing must
treat the lane as candidate URL intake, not broad Reddit crawling.

Implementation authorized by this artifact: no. Later owner direction authorizes
the smallest bounded live old Reddit Candidate URL Intake runner when a per-run
envelope and explicit live-access authorization are present.

Live Reddit access, dependency installation, runner dispatch, Source Capture
Packet generation, storage, dashboard, scheduler, deployment, production
runtime, ECR, Cleaning, Judgment, fixture admission, source-quality scoring, or
commercial Reddit use authorized by this artifact alone: no.

## Implementation Status

Local support exists under:

- `orca-harness/capture_spine/reddit_candidate_intake/`
- `orca-harness/runners/run_reddit_candidate_intake_live.py`

The live runner is the bounded first-contact Reddit sourcing path when the
operator supplies an explicit run envelope and live access is authorized for
that run. It fetches one declared source URL transiently, then writes candidate
subreddit/thread rows, provenance, and a live-run receipt only. It does not
persist raw source, invoke Source Capture Armory, emit Source Capture Packets,
auto-promote candidates, traverse newly found subreddits, or capture
bodies/comments/profiles.

## Source Context Status

`SOURCE_CONTEXT_READY` for architecture doctrine and docs-write. The workspace
is dirty and several adjacent files are modified or untracked, so this artifact
does not claim validation, readiness, source freshness for every adjacent file,
or clean-tree acceptance.

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom Data Capture Spine / Source Capture Armory / Reddit candidate-intake pack
  edit_permission: docs-write
  target_scope:
    - docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
  dirty_state_checked: yes
  blocked_if_missing: none for this architecture write
```

Primary grounding sources:

- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/decision-routing.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/retrieval-metadata.md`
- `docs/workflows/data_capture_spine_consolidation_map_v0.md`
- `docs/product/data_capture_spine_candidate_url_intake_contract_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
- `docs/product/data_capture_source_access_boundary_decision_v0.md`
- `docs/product/data_capture_source_access_method_plan_v0.md`
- `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md`
- `docs/product/source_capture_toolbox/README.md`
- `docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md`
- `docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md`
- `orca-harness/docs/source_capture_agent_runbook.md`

## Goal Fit

This artifact serves the thread-local goal of giving the operator-facing Reddit
crawler a safe Capture Spine home without authorizing broad crawling, body
capture, packets, or implementation.

Success is not the existence of a file alone. Success is that a future agent can
tell the following apart without re-litigating the boundary:

- bounded candidate URL intake;
- Source Capture Armory packet capture;
- commissioned Data Capture under a Decision Frame;
- ECR, Cleaning, Judgment, fixture admission, and source-quality scoring.

## Cynefin Routing Result

Smallest complete outcome: write a durable architecture contract and sub-map
route for bounded Reddit Candidate URL Intake, without implementation.

Regime: complicated with a bounded complex edge.

Why: existing sources define the Data Capture, Armory, Reddit capture, and
candidate/scouting boundaries, but the candidate URL intake destination was an
explicit gap.

Decomposition: layer-based, with a risk-first guard around the
enumeration-versus-broad-discovery boundary.

Current bottleneck: candidate URL rows must not become Data Capture handoff,
Source Capture Packets, or broad crawler output by implication.

Riskiest assumption: bounded listing/search enumeration inside declared caps is
architecturally distinct from broad Reddit crawling.

Stop or pivot condition: if the desired behavior requires same-run traversal
from candidate surfaces into newly found subreddits, threads, outbound pages,
users, comments, links, recommendations, "more like this" surfaces, indefinite
monitoring, body/comment capture, or persistent crawl infrastructure, this
contract is the wrong lane.

Allowed next move: bounded implementation scoping or execution only when a
run envelope and live-access authorization are explicitly supplied.

Disallowed next move: unbounded live Reddit access, Source Capture Armory
runner dispatch, Source Capture Packet generation, Data Capture handoff, or
broad crawler build authorization.

## Architecture Recommendation

`TARGET_RECOMMENDED`.

Bounded Reddit Candidate URL Intake belongs under **Capture Spine Candidate URL
Intake**, upstream of commissioned Data Capture and outside Source Capture
Armory.

It is a pre-promotion candidate enumeration lane. It may produce candidate
subreddit rows and candidate thread URL rows with provenance. It must not
preserve source bodies, comments, screenshots, raw HTML, profile data, hidden
session state, parser output, Source Capture Packets, ECR rows, Cleaning
outputs, Judgment inputs, fixture-admission records, or source-quality scores.

For the first old-Reddit implementation slice, static no-live projection remains
old Reddit HTML listing/search/sidebar content. Live intake is governed by the
explicit run envelope and the candidate-only output contract rather than
runner-local source-shape allowlists. The lane may transiently project fetched source
content into candidate rows in memory, but it must not persist raw HTML, parser
output, thread body text, comments, user/profile data, or raw Reddit payloads.

Source Capture Armory may later consume a promoted URL as a downstream execution
option. This intake lane does not invoke Armory by default.

For promoted Reddit capture, the source-backed downstream access posture is:
CloakBrowser is the approved primary anti-blocking browser route for bounded
pre-commercial Reddit capture, old Reddit HTML is preferred where available,
and residential or rotating proxies are not blanket stop conditions inside the
pre-commercial/free anti-blocking posture. This posture prevents future lanes
from re-litigating whether CloakBrowser/proxy-backed capture is allowed, but it
does not make Candidate URL Intake a browser, proxy, or packet runner.

## Directional Lane

The intended lane shape is a thin candidate-intake surface:

1. The operator declares a bounded Reddit topic, theme, query, or subreddit
   scope.
2. The run applies hard caps and exclusions before any access.
3. The run records listing/search provenance and stop reason.
4. The run emits only candidate subreddit rows and candidate thread URL rows.
5. Every row starts as `candidate_or_scouting`.
6. A separate promotion gate is required before any URL can become a capture
   unit.

This is the missing upstream destination for candidate/scouting material. It is
not the existing Reddit pre-commercial capture/consolidation thread, because
that thread is packet-before-parser capture planning inside the Armory-adjacent
source-capture world.

## Adversarial Lane

The main failure modes are boundary leaks:

1. **Broad crawl drift.** A bounded run treats newly found subreddits,
    cross-posts, recommendations, related surfaces, sidebar markdown related
    links, "more like this" surfaces, or outbound links as permission to continue
    traversal inside the same run. Hard stop: those surfaces may produce
    candidate rows only when declared and capped; entering or following them
    requires a new declared run, scope amendment, or promotion gate.

2. **Body capture by stealth.** The lane fetches enough thread/comment body text
   to rank, score, or qualify candidates. Hard stop: no body/comment text is an
   output or intermediate retained artifact of this lane.

3. **Armory laundering.** The lane writes a Source Capture Packet or invokes a
   packet runner. Hard stop: candidate intake emits rows and receipts only; a
   packet begins only after promotion.

4. **Data Capture laundering.** Candidate rows are treated as Data Capture handoff
   input. Hard stop: a candidate row is `candidate_or_scouting` until a separate
   promotion gate binds it to a Decision Frame or approved capture unit.

5. **Retry escalation.** Empty or blocked results trigger broader crawling.
   Hard stop: empty-result and blocked-result are valid terminal outcomes with a
   visible stop reason.

6. **Monitoring drift.** A small monitored set becomes indefinite production
   monitoring. Hard stop: monitored runs require a cadence, stop date, and cap;
   otherwise the run fails the boundary gate.

7. **Secret-bearing output.** Browser/session material enters the artifact.
   Hard stop: credentials, cookies, browser profiles, storage-state, session
   sidecars, authorization headers, and secrets must not appear in rows,
   receipts, or sidecars.

8. **Commercial drift.** Pre-commercial candidate intake becomes commercial
   Reddit acquisition. Hard stop: commercial, client-funded, buyer-facing,
   enterprise, scale, or data-licensing pressure stops this lane and reroutes to
   the sanctioned commercial/API path before further work.

## Grounding Lane

| Proposed element | Existing authority or status | Verdict |
| --- | --- | --- |
| Lane outside Source Capture Armory | Armory README defines Armory around Source Capture Packet-producing capture paths. | Grounded. |
| Candidate/scouting default | Reddit planning thread classifies `candidate_or_scouting` units and names their missing handoff destination. | Grounded. |
| Data Capture requires Decision Frame | Data Capture obligation contract applies to commissioned capture and rejects standing/opportunistic corpus capture inside v0. | Grounded. |
| URL enumeration may be conceptually in-bounds | Source-access boundary distinguishes fast discovery from evidence-grade material use. | Grounded, not build authorization. |
| Broad crawler/spider and SERP/discovery API builds remain deferred | Source-access tooling build authorization defers broad crawler/spider frameworks and SERP/discovery APIs. | Grounded hard stop for implementation. |
| Generic candidate locator rows, run envelope, caps, and promotion gate | Parent Candidate URL Intake contract. | Grounded by parent contract. |
| Reddit candidate subreddit/thread/outbound URL rows | Parent row contract plus Reddit-specific source surfaces and field names. | Reddit specialization of the parent contract. |
| Sort order and exclusion receipt | Method provenance already required generally; these are candidate-intake sub-fields. | New required sub-fields. |
| Promotion gate | Data Capture Commissioning Gate plus Reddit candidate/scouting gap. | Grounded, named here. |
| No packets / no body / no comments | Armory packet boundary and Data Capture forbidden-output discipline. | Grounded and tightened here. |
| No user/profile capture | Boundary hard stops and ordinary-person dossier concern. | Grounded and tightened here. |

## Lane Contract

### Reddit Graph Frontier Boundary

Owner direction accepts a separate agent-mediated **Reddit Graph Frontier Lane**
with a **Graph Frontier Register**. That lane may choose the next frontier node
and prepare the next bounded run, but every hop requires a new `run_id`, declared
surface, caps, exclusions, access mode, source-policy posture, and stop
condition.

That lane is not this Candidate URL Intake lane. Candidate URL Intake may supply
structural candidate rows to the Graph Frontier Register, but it does not score,
rank, suppress, select, enter, or traverse discovered nodes. This artifact's
no-broad-crawling and no-same-run-traversal rules remain binding for Candidate
URL Intake.

The owning contract is:

`docs/product/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md`

### Ownership

Owner lane: **Capture Spine Candidate URL Intake**.

Not owner lanes:

- Source Capture Armory;
- Source Capture Packet lifecycle;
- commissioned Data Capture;
- ECR;
- Cleaning;
- Judgment;
- source-quality scoring;
- fixture admission.

### Required Inputs

A run is invalid unless these are declared before execution:

- `run_id`;
- `declared_topic_theme_or_query`;
- optional `seed_subreddits`;
- `max_subreddits`;
- `max_threads_per_subreddit`;
- `max_pages_or_result_surfaces`;
- `time_window`;
- `sort_order`;
- `exclusions`;
- `run_purpose`;
- `non_commercial_posture`;
- `source_surface`;
- `method_category`;
- `stop_condition`;
- `candidate_surface_allowlist`;
- caps for each allowed candidate surface, including related subreddit,
  sidebar markdown related links, recommendation, cross-post, "more like this",
  and outbound-link surfaces when those surfaces are in scope;
- optional `monitoring_cadence` only with a hard `stop_date`.

### Outputs

Allowed output row types:

1. Candidate subreddit row.
2. Candidate thread URL row.
3. Outbound URL candidate row.
4. Run-level provenance receipt.

Candidate subreddit row fields:

- `run_id`;
- `capture_unit_intake_status`: always `candidate_or_scouting` unless a later
  promotion receipt changes it outside this lane;
- `source_family`: `reddit`;
- `subreddit_name`;
- `subreddit_url`;
- `declared_topic_theme_or_query`;
- `source_surface`;
- `query_or_listing_path`;
- `sort_order`;
- `time_window`;
- `enumeration_timestamp`;
- `method_category`;
- `approved_downstream_access_route_or_none`;
- `exclusion_receipt`;
- `visible_subscriber_count_or_none`;
- `visible_active_user_count_or_none`;
- `visible_volume_signal_absent_reason_or_none`;
- `visible_stop_reason_if_any`;
- `allowed_downstream_use`: default `planning_only`.

Candidate subreddit rows may come from declared Reddit search/listing surfaces,
cross-post surfaces, recommendation surfaces, related-subreddit surfaces,
sidebar markdown related links, or "more like this" surfaces only when that
surface is named in
`candidate_surface_allowlist` and capped before the run. A discovered subreddit
must not be entered for thread enumeration inside the same run. It becomes input
to a later bounded run only after an explicit scope amendment or new `run_id`.

Visible subscriber and active-user counts are allowed provenance fields only
when the declared source surface visibly exposes them. They must not be inferred
from search rank, thread count, memory, hidden metadata, browser account chrome,
or unrelated navigation. If the source surface does not visibly expose volume,
record a volume-absent reason instead of inventing a count.

Candidate subreddit projection must remove non-candidate subreddit links before
row emission. Reject header navigation, "my subreddits", popular/all bars,
footer links, account menus, preferences, moderator/report templates, and other
page chrome unless the run explicitly declares that surface and cap. Projection
may keep only the declared candidate surface, such as related subreddit, sidebar
markdown related links, recommendation, cross-post, "more like this", or
subreddit search result.

Candidate thread URL row fields:

- `run_id`;
- `capture_unit_intake_status`: always `candidate_or_scouting` unless a later
  promotion receipt changes it outside this lane;
- `source_family`: `reddit`;
- `subreddit_name`;
- `thread_url`;
- `thread_permalink_or_locator`;
- `visible_listing_title_or_none`;
- `visible_listing_timestamp_or_none`;
- `visible_listing_score_state_or_none`;
- `declared_topic_theme_or_query`;
- `source_surface`;
- `query_or_listing_path`;
- `sort_order`;
- `time_window`;
- `enumeration_timestamp`;
- `method_category`;
- `approved_downstream_access_route_or_none`;
- `exclusion_receipt`;
- `visible_stop_reason_if_any`;
- `allowed_downstream_use`: default `planning_only`.

Thread URL rows may point to cross-posted or recommended threads only when the
cross-post or recommendation surface is declared and capped. The row is still a
candidate URL only; the run must not follow into the target thread body, comment
tree, user profile, or linked subreddit inside the same run.

Outbound URL candidate row fields:

- `run_id`;
- `capture_unit_intake_status`: always `candidate_or_scouting` unless a later
  promotion receipt changes it outside this lane;
- `source_family`: `reddit`;
- `source_reddit_thread_url_or_locator`;
- `outbound_url`;
- `visible_listing_anchor_or_context_or_none`;
- `declared_topic_theme_or_query`;
- `source_surface`;
- `query_or_listing_path`;
- `sort_order`;
- `time_window`;
- `enumeration_timestamp`;
- `method_category`;
- `approved_downstream_access_route_or_none`;
- `exclusion_receipt`;
- `requires_separate_source_family_intake`: `yes`;
- `visible_stop_reason_if_any`;
- `allowed_downstream_use`: default `planning_only`.

Outbound URL candidates must not be fetched, rendered, archived, summarized, or
packetized inside Reddit Candidate URL Intake. A separate promotion or
source-family intake decision owns any later access to the outbound source.

Run-level provenance receipt fields:

- `run_id`;
- declared inputs;
- caps applied;
- exclusions applied;
- source surface;
- query/listing path;
- sort order;
- time window;
- method category;
- timestamp;
- row counts;
- stop reason;
- empty-result or blocked-result state, if applicable;
- non-commercial posture;
- non-claims.

### Explicit Non-Outputs

This lane must not output, preserve, derive, or imply:

- thread body text;
- comment body text;
- user profile data;
- ordinary-person dossier data;
- hidden session state;
- credentials, cookies, browser profiles, storage-state, session sidecars,
  authorization headers, or secrets;
- raw HTML;
- screenshots;
- parser output;
- Source Capture Packets;
- packet lifecycle state;
- fixture admission or fixture recommendation;
- ECR rows or fields;
- Cleaning transformations;
- Judgment inputs, scores, or classifications;
- source-quality result tokens;
- credibility, relevance, inclusion, exclusion, sentiment, or quality decisions;
- commercial-use claims.

### Promotion Model

Candidate rows are inert planning context.

A candidate URL may become a capture unit only through a separate promotion gate
that records:

- the exact URL being promoted;
- the Decision Frame or approved capture-unit authority;
- the capture purpose;
- the selected downstream capture method;
- the non-promotion of all non-selected candidate rows;
- the fact that Source Capture Armory execution has not happened yet.

Promotion does not itself capture the source. It only makes the URL eligible for
a later authorized capture path.

### Stop Model

Valid terminal run outcomes:

- `caps_reached`;
- `scope_exhausted`;
- `empty_result`;
- `blocked_result`;
- `operator_stop`;
- `hard_stop_triggered`;
- `commercial_reroute_required`.

Every run records one visible stop reason. Empty-result and blocked-result are
valid outcomes. A stop reason must not trigger automatic silent scope widening.

Cap semantics:

- A cap is a bounded-work stop, not a sufficiency claim.
- `caps_reached` means only that the declared run stopped at its declared cap.
- It must not be reported as `done`, `complete`, `topic covered`, or "no more
  relevant candidates."
- The run must record `coverage_claim`.

Allowed `coverage_claim` values:

- `bounded_probe_only`;
- `bounded_batch_only`;
- `high_recall_attempt_with_limits`.

Allowed `cap_type` values:

- `probe`;
- `working_batch`;
- `high_recall_pass`.

Continuation or widening is allowed only as a new declared run or explicit scope
amendment. The continuation must preserve the prior stop reason and record the
changed field: cap, time window, sort order, source surface, seed subreddit,
candidate surface, or exclusion rule. It must not mutate the prior run in place.

### Method Provenance

Every run and candidate row records:

- source surface;
- query or listing path;
- sort order;
- time window;
- enumeration timestamp;
- method category;
- approved downstream access route, if already source-backed;
- exclusion receipt;
- caps applied;
- cap type;
- coverage claim;
- stop reason;
- non-commercial posture.

Method provenance is a traceability requirement only. It is not validation,
source adequacy, rights clearance, evidence-grade provenance, or material-use
authorization.

### Armory Bridge

Source Capture Armory tools may consume a promoted URL later. The default bridge
is one promoted URL into a downstream capture path that can preserve source
material in a Source Capture Packet.

For Reddit, the approved primary downstream capture route is CloakBrowser
anti-blocking capture over bounded pre-commercial Reddit source sets, with
**old Reddit first** as the default surface posture for future promoted capture.
New Reddit surfaces are non-default and require separate scope amendment or
later owner decision. Residential or rotating proxies are allowed inside that
pre-commercial anti-blocking posture and are not blanket stop conditions. The
hard stops remain stolen or nonconsensual credentials, raw
cookie/profile import, no-entitlement bypass, obvious private/admin spillover
once noticed, broad crawler/spider frameworks, commercial fetch, standalone
CAPTCHA-solving services, storage, dashboard, scheduler, deployment, production
runtime, and ECR/Cleaning/Judgment behavior.

This intake lane does not invoke Armory by default. It does not call
CloakBrowser, proxy configuration, Reddit API, browser snapshot, archive,
parser, source-quality, or state-assembler runners. The bounded live intake
runner may fetch one declared source URL as first-contact sourcing, but
promoted capture still belongs to a separate downstream lane. It may record
`approved_downstream_access_route_or_none: cloakbrowser_primary_anti_blocking`
as provenance or promotion context when that route is already source-backed.

### Subagent Boundary

Subagents may be used only as bounded intake workers inside one declared run.
They inherit the run envelope; they do not define or expand it.

Allowed subagent roles:

- scope-check worker: verifies required inputs, caps, exclusions, stop condition,
  and non-commercial posture are present;
- bounded enumeration worker: inspects one assigned source surface inside the
  declared cap and returns candidate rows plus provenance only;
- adversarial boundary worker: checks for body/comment/profile leakage, hidden
  session state, missing stop reason, same-run traversal, cap-as-completion
  language, or auto-promotion;
- consolidation worker: merges candidate rows and preserves empty, blocked,
  capped, and hard-stop outcomes.

Subagents must not choose additional surfaces, widen scope, follow candidates,
fetch bodies, capture packets, rank candidates, score source quality, or promote
URLs.

## Success Signals

A bounded Reddit Candidate URL Intake run is architecturally in-bounds only when
all applicable signals are checkable:

- bounded topic/subreddit/thematic scope is mandatory before any run;
- hard caps exist for subreddits, threads per subreddit, pages/result surfaces,
  time window, and stop condition;
- every run records a visible stop reason;
- empty-result and blocked-result are valid terminal outcomes;
- no retry escalation into broad crawling;
- `caps_reached` is not a sufficiency claim and carries `cap_type` plus
  `coverage_claim`;
- continuation or widening records a new run or scope amendment with the prior
  stop reason preserved;
- related subreddits, recommendations, cross-posts, and "more like this"
  surfaces can produce candidate rows only when declared and capped; they do not
  authorize same-run traversal;
- outbound links can produce outbound URL candidate rows only; they are not
  fetched inside Reddit Candidate URL Intake;
- every candidate records source surface, query, sort, window, timestamp,
  method category, caps, and exclusion receipt;
- output is candidate subreddit/thread/outbound URLs plus provenance only;
- no body/comment/profile capture;
- no hidden session or secret-bearing output;
- no Source Capture Packet output;
- no auto-promotion into capture units;
- no Data Capture handoff claim without a Decision Frame or approved capture
  unit;
- no ECR, Cleaning, Judgment, fixture admission, source-quality scoring, or
  commercial-use claim;
- handoff occurs only through a promotion gate into approved capture units.

## Non-Goals And Hard Stops

Non-goals:

- Reddit body capture;
- Reddit comment capture;
- Reddit profile/user capture;
- broad Reddit crawling;
- same-run traversal from candidate discovery surfaces;
- Source Capture Packet emission;
- parser/consolidation runner implementation;
- durable corpus or database creation;
- queue, scheduler, dashboard, deployment, or production runtime;
- commercial Reddit acquisition;
- ECR, Cleaning, Judgment, fixture admission, or source-quality scoring.

Hard stops:

- site-wide Reddit walking;
- generic subreddit harvesting without a declared topic/theme/query and caps;
- entering or following discovered users, profiles, comments, links,
  recommendations, cross-posts, related surfaces, outbound URLs, or "more like
  this" surfaces inside the same run;
- treating `caps_reached`, `empty_result`, or `blocked_result` as completion,
  sufficiency, or topic coverage;
- no-entitlement gate bypass;
- stolen or nonconsensual credentials, cookies, or sessions;
- security exploits, malware, credential stuffing, or obvious cross-account,
  private, admin, or confidential spillover once noticed;
- any method Orca would refuse to disclose internally;
- any secret-bearing row, receipt, or sidecar;
- monitored scope without both cadence and hard stop date;
- commercial, client-funded, buyer-facing, enterprise, scale, or data-licensing
  pressure before rerouting to sanctioned commercial/API paths.

## Artifact Placement

This artifact belongs at:

`docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md`

It intentionally does not live under:

`docs/product/source_capture_toolbox/`

That folder is the Source Capture Armory product-doc home. Putting candidate URL
intake there would blur the boundary and make the lane look like a packet
capture tool.

The Data Capture consolidation sub-map must route to this artifact. The top-level
repo map may remain thin unless a later owner decision makes this artifact a
primary entrypoint.

## Open Owner Questions

This artifact now routes default-policy questions to
`docs/decisions/data_capture_spine_reddit_candidate_url_intake_default_policy_decision_v0.md`.

Remaining questions do not block architecture placement. They block owner
acceptance of default policy, implementation scoping, or promotion mechanics:

1. Should the parent Candidate URL Intake contract later be superseded by a
   broader Candidate Signal Intake / Corpus Intake contract that owns all
   pre-Decision-Frame candidate material, including non-URL signals?
2. Does the owner accept the recommended default caps by `cap_type`?
3. Does the owner accept the recommended default-on/default-off candidate
   surfaces and outbound-link opt-in policy?
4. Does the owner accept monitored Reddit scopes as default-off before a Decision
   Frame?
5. Does the owner accept operator-owned Candidate URL Intake promotion receipts
   until Data Capture commissioning accepts a promoted unit?
6. Does the owner accept visible listing title/timestamp/score-state as
   provenance-only fields by default?

## Next Authorized Step

Allowed next step after this artifact: bounded old Reddit Candidate URL Intake
execution with a per-run envelope, or owner review of
`docs/decisions/data_capture_spine_reddit_candidate_url_intake_default_policy_decision_v0.md`.

Bounded live-access implementation or execution may proceed only after:

1. owner acceptance of this architecture contract;
2. owner acceptance of the Reddit Candidate URL Intake default-policy decision;
3. owner acceptance of the parent Candidate URL Intake contract;
4. confirmation that the scoped design uses old Reddit first for Reddit URL
   normalization and live first-contact sourcing unless separately amended;
5. confirmation that the scoped design avoids deferred broad crawler/spider,
   SERP/discovery API, storage, scheduler, dashboard, production runtime, and
   thread-body capture surfaces unless separately authorized;
6. a concrete run envelope records run id, purpose, declared topic/query/seed,
   source surface, caps, exclusions, access mode, source-policy posture, and
   stop condition.

Source Capture Armory execution, promoted capture runner dispatch, or use of
the existing CloakBrowser/proxy substrate remains a separate downstream
authorization.

## Non-Claims

This artifact is not validation, readiness, source-access boundary amendment,
legal sufficiency, rights clearance, broad implementation authorization,
unbounded live Reddit authorization, Source Capture Armory authorization, Source Capture Packet
generation, Data Capture handoff, ECR design, Cleaning design, Judgment design,
fixture admission, source-quality scoring, buyer proof, commercial Reddit
authorization, storage authorization, dashboard authorization, scheduler
authorization, deployment authorization, production-runtime authorization,
commit authorization, push authorization, or PR authorization.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "Orca now has a bounded Reddit Candidate URL Intake architecture contract under Capture Spine: it permits provenance-only candidate subreddit/thread/outbound URL rows, allows declared-and-capped related-surface candidate discovery without same-run traversal, permits transient old Reddit HTML listing/search projection into candidate rows only, records old Reddit first plus CloakBrowser as the approved primary downstream anti-blocking route and proxies as not blanket stop conditions for pre-commercial capture without making intake invoke or set them up, treats caps as stop/coverage metadata rather than sufficiency, and forbids broad crawling, body/comment/profile capture, raw HTML or parser-output persistence, Source Capture Packet output, automatic Data Capture handoff, ECR/Cleaning/Judgment behavior, source-quality scoring, and implementation execution by implication."
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
    - output_authority
    - product_doctrine
  controlling_sources_updated:
    - "docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md"
    - "docs/decisions/data_capture_spine_reddit_candidate_url_intake_default_policy_decision_v0.md"
    - "docs/product/data_capture_spine_candidate_url_intake_contract_v0.md"
    - "docs/workflows/data_capture_spine_consolidation_map_v0.md"
    - "docs/decisions/data_capture_spine_reddit_candidate_url_intake_default_policy_decision_v0.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/decision-routing.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - ".agents/workflow-overlay/retrieval-metadata.md"
    - "docs/workflows/data_capture_spine_consolidation_map_v0.md"
    - "docs/product/data_capture_spine_candidate_url_intake_contract_v0.md"
    - "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
    - "docs/product/data_capture_source_access_boundary_decision_v0.md"
    - "docs/product/data_capture_source_access_method_plan_v0.md"
    - "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
    - "docs/product/source_capture_toolbox/README.md"
    - "docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md"
    - "docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md"
    - "orca-harness/docs/source_capture_agent_runbook.md"
  intentionally_not_updated:
    - path: "docs/workflows/orca_repo_map_v0.md"
      reason: "The top-level repo map already routes Data Capture detail through the Data Capture consolidation sub-map. This new artifact is discoverable through that sub-map; a top-level map expansion would duplicate sub-map detail."
    - path: "docs/product/source_capture_toolbox/README.md"
      reason: "The new lane is explicitly not Source Capture Armory. Adding it to the Armory README would blur ownership; the sub-map route is the correct bridge."
    - path: "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
      reason: "Commissioned-capture obligations did not change. This artifact stays upstream of the Commissioning Gate and does not amend Data Capture obligations."
    - path: "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
      reason: "Build authorization did not change. Broad crawler/spider, SERP/discovery API, storage, scheduler, dashboard, deployment, production runtime, and unbounded live Reddit execution remain separately gated."
    - path: "orca-harness/docs/source_capture_agent_runbook.md"
      reason: "No runner behavior changed. Existing runner guidance remains one supplied URL for packet capture and does not gain candidate-intake enumeration authority."
  stale_language_search: "rg -n \"Candidate URL Intake|candidate URL intake|crawler|broad crawler|Source Capture Packet output|auto-promotion|candidate_or_scouting|caps_reached|coverage_claim|outbound URL|same-run traversal|subagent|old Reddit first|old-Reddit-first|transient old Reddit HTML|raw HTML|parser output|CloakBrowser/proxy setup|implementation execution\" docs/product/data_capture_spine_candidate_url_intake_contract_v0.md docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md docs/workflows/data_capture_spine_consolidation_map_v0.md docs/product/source_capture_toolbox/README.md docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md orca-harness/docs/source_capture_agent_runbook.md"
  stale_language_search_result: "Superseded by later owner direction allowing the bounded live runner to rely on the run envelope and candidate-only output contract rather than runner-local input-surface allowlists."
  non_claims:
    - "not validation"
    - "not readiness"
    - "not source-access boundary amendment"
    - "not implementation authorization"
    - "not unbounded live Reddit authorization"
    - "not broad crawling authorization"
    - "not Source Capture Packet generation"
    - "not ECR, Cleaning, Judgment, fixture admission, source-quality scoring, or commercial Reddit authorization"
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Candidate URL Intake now points to the accepted Reddit Graph Frontier Lane
    as a separate downstream/sibling frontier lane, while preserving Candidate
    URL Intake as structural row/provenance output only with no semantic scoring
    and no same-run traversal.
  trigger: architecture_doctrine
  related_triggers:
    - output_authority
    - lifecycle_boundary
  controlling_sources_updated:
    - "docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md"
    - "docs/product/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md"
    - "docs/workflows/reddit_candidate_intake_to_projection_lane_handoff_v0.md"
    - "docs/workflows/data_capture_spine_consolidation_map_v0.md"
    - "docs/workflows/orca_repo_map_v0.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/decision-routing.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - "docs/workflows/reddit_candidate_intake_old_reddit_search_surface_handling_v0.md"
    - "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
  intentionally_not_updated:
    - path: "docs/product/source_capture_toolbox/README.md"
      reason: "The Graph Frontier Lane is not Source Capture Armory and does not emit Source Capture Packets."
    - path: "orca-harness/docs/source_capture_agent_runbook.md"
      reason: "No runner behavior changed and this patch does not authorize implementation execution."
  stale_language_search: "rg -n \"Graph Frontier|crawler-graph|crawler graph|same-run traversal|semantic scoring|Source Capture Packet|Data Capture handoff\" docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md docs/product/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md docs/workflows/reddit_candidate_intake_to_projection_lane_handoff_v0.md docs/workflows/data_capture_spine_consolidation_map_v0.md docs/workflows/orca_repo_map_v0.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not live Reddit authorization"
    - "not implementation authorization"
    - "not Source Capture"
    - "not Data Capture"
```
