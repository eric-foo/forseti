# Data Capture Spine Reddit Candidate URL Intake Default Policy Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Product decision
scope: Recommended default policy for bounded Reddit Candidate URL Intake caps, candidate surfaces, outbound links, monitored runs, continuation, promotion ownership, and implementation-scoping gate.
use_when:
  - Deciding default run policy for the operator-facing Reddit Candidate URL Intake crawler.
  - Scoping a no-live-access implementation after owner acceptance of default caps and surfaces.
  - Checking whether a Reddit intake run may widen, monitor, emit outbound candidates, or promote URLs.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_candidate_url_intake_contract_v0.md
  - forseti/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
stale_if:
  - The parent Candidate URL Intake contract changes cap, coverage, continuation, outbound, or promotion rules.
  - The Reddit Candidate URL Intake architecture changes candidate surfaces, row fields, or hard stops.
  - Reddit source-access ordering, CloakBrowser/proxy allowance, or commercial reroute rules change.
  - A later owner decision accepts, rejects, or supersedes these defaults.
```

## Status

Status: `RECOMMENDED_DEFAULT_POLICY_PENDING_OWNER_ACCEPTANCE`.

This artifact proposes the smallest complete default policy needed before
bounded Reddit Candidate URL Intake implementation scoping can proceed without
inventing product policy.

It is not an implementation authorization. It is not live Reddit authorization.
It is not Source Capture Armory authorization. It does not authorize
CloakBrowser/proxy invocation or reconfiguration, Source Capture Packet
generation, body or comment capture, storage, scheduler, dashboard, deployment,
production runtime, commercial Reddit acquisition, ECR, Cleaning, Judgment,
fixture admission, or source-quality scoring.

Owner acceptance required before implementation scoping may treat these values
as locked: yes.

## Source Context Status

`SOURCE_CONTEXT_READY` for docs-only default-policy recommendation. This
artifact does not claim validation, readiness, clean-tree state, runtime
feasibility, owner acceptance, legal sufficiency, or source-access boundary
amendment.

Primary grounding sources:

- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/decision-routing.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/retrieval-metadata.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `docs/product/data_capture_spine_candidate_url_intake_contract_v0.md`
- `docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md`
- `docs/workflows/data_capture_spine_consolidation_map_v0.md`
- `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md`
- `docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md`

## Smallest Complete Assessment

The smallest complete foundational default-policy artifact must lock only the
policy fields that would otherwise be invented during implementation scoping:

- default run modes and caps;
- default candidate surfaces;
- outbound-link posture;
- monitored/repeated-run posture;
- continuation and widening rule;
- promotion receipt owner;
- listing-provenance posture;
- implementation-scoping gate.

Out of scope for this artifact:

- implementation route;
- live Reddit access;
- new CloakBrowser or proxy setup in this lane;
- Source Capture Armory runner behavior;
- promotion-gate schema beyond ownership and required authority;
- storage, queue, scheduler, dashboard, deployment, or production runtime;
- ECR, Cleaning, Judgment, fixture admission, source-quality scoring, or
  commercial Reddit use.

## Cynefin And Fused Routing

Smallest complete outcome: recommend one bounded default policy decision and
patch the Reddit architecture and Data Capture sub-map so future scoping can
find it.

Regime: complicated.

Why: the parent and Reddit-specific architecture already define the lane; the
remaining uncertainty is source-family default policy, not architecture.

Decomposition: layer-based. This decision owns Reddit default policy only. The
parent contract owns generic Candidate URL Intake. The Reddit architecture owns
source-family lane shape. Source Capture Armory owns downstream packet capture.

Current bottleneck: implementation scoping would otherwise invent caps, default
surfaces, outbound-link behavior, monitoring posture, and promotion ownership.

Riskiest assumption: default caps can be useful while carrying no sufficiency or
topic-coverage claim.

Stop or pivot condition: if these defaults are meant to authorize live source
access, body capture, broad crawling, CloakBrowser/proxy invocation or
reconfiguration, packet generation, or commercial acquisition, this artifact is
the wrong lane.

Allowed next move: owner accept, reject, or patch these defaults; then, if
accepted, separately authorize no-live-access implementation scoping.

Disallowed next move: runtime implementation, live Reddit access, same-run
traversal, Source Capture Packet output, or Data Capture handoff by implication.

Fused lane result for this turn: `/fused` is narrowed to non-code
artifact-writing. Runtime implementation is blocked. Spec writing is satisfied
by the decision fields below. Micro-decision locking freezes the patch boundary:
one default-policy artifact plus minimal route patches only.

## Decision

Recommended decision: `TARGET_RECOMMENDED`.

Adopt the following defaults for bounded pre-commercial Reddit Candidate URL
Intake unless the owner accepts different values in a later decision.

These caps are maximum default limits, not targets. A run may choose lower caps.
Exceeding these caps requires an explicit scope amendment or later owner
decision. No cap is evidence of sufficiency, coverage, topic completion, source
adequacy, or high recall by itself.

## Default Run Modes And Caps

| `cap_type` | `coverage_claim` | Default max subreddits | Default max threads per subreddit | Default max pages/result surfaces per allowed surface | Default time window | Use when |
| --- | --- | ---: | ---: | ---: | --- | --- |
| `probe` | `bounded_probe_only` | 5 | 25 | 2 | 30 days unless operator declares narrower | Testing whether the declared topic/surface yields candidate URLs. |
| `working_batch` | `bounded_batch_only` | 20 | 75 | 5 | 180 days unless operator declares narrower | Ordinary bounded intake for planning a later promotion decision. |
| `high_recall_pass` | `high_recall_attempt_with_limits` | 50 | 150 | 10 | 365 days unless operator declares narrower | Explicit attempt to reduce missed candidates while preserving hard stops. |

Default mode when unspecified: `probe`.

`high_recall_pass` is not the default. It requires an explicit operator-selected
run purpose and must preserve the `high_recall_attempt_with_limits` claim.

Every run records:

- selected `cap_type`;
- selected `coverage_claim`;
- declared caps;
- row counts;
- stop reason;
- continuation or widening status.

## Default Candidate Surfaces

Default-on surfaces:

- operator-declared seed subreddits;
- declared Reddit search/listing surface for the declared topic/theme/query;
- declared subreddit listing surface;
- cross-post surface, as candidate rows only;
- related-subreddit surface, as candidate subreddit rows only.

Default-off unless explicitly allowlisted:

- recommendation surfaces;
- "more like this" surfaces;
- outbound-link surfaces;
- monitored or repeated-run surfaces;
- any source surface that requires following users, profiles, comments, or
  relationship chains.

Default-off does not mean forbidden. It means the operator must declare the
surface in `candidate_surface_allowlist`, set a surface-specific cap, and accept
that same-run traversal remains forbidden.

Default-on does not mean uncapped or exempt from the parent allowlist-and-cap
rule. The default-on cross-post and related-subreddit surfaces are included in
the default `candidate_surface_allowlist` and remain capped: discovered
candidate subreddit rows count against `Default max subreddits`, and cross-post
candidate thread rows count against `Default max threads per subreddit` and
`Default max pages/result surfaces`. An operator may set a tighter
surface-specific cap but may not exceed these caps without a scope amendment or
later owner decision. Producing a candidate row for a discovered cross-post or
related subreddit never authorizes same-run traversal into it; entering it
requires a new `run_id` or an explicit scope amendment.

## Outbound Link Policy

Outbound links are default-off.

They may be enabled only when:

- `candidate_surface_allowlist` includes `outbound_links`;
- the run purpose explains why outbound sources may matter;
- an outbound-link cap is declared;
- every outbound row records `requires_separate_source_family_intake: yes`;
- no outbound URL is fetched, rendered, archived, summarized, packetized,
  ranked, or scored inside Reddit Candidate URL Intake.

Default outbound cap when explicitly enabled:

- `probe`: 25 outbound URL candidate rows total;
- `working_batch`: 100 outbound URL candidate rows total;
- `high_recall_pass`: 250 outbound URL candidate rows total.

These caps are row caps only. They do not authorize access to outbound sources.

## Monitoring And Repeated Runs

Default posture: monitored Reddit scopes are disabled before a Decision Frame.

Allowed default alternative: repeated manual runs with new `run_id` values,
explicit run purpose, declared caps, and preserved prior stop reasons.

Monitoring before a Decision Frame requires a separate owner decision or scope
amendment that names:

- cadence;
- hard `stop_date`;
- maximum number of runs;
- maximum rows per run;
- commercial-reroute stop;
- why monitoring is still candidate intake rather than production tracking.

No monitored run may become scheduler, dashboard, storage, production runtime,
commercial acquisition, or Data Capture handoff by implication.

## Continuation And Widening

Continuation is allowed only as:

- a new run with a new `run_id`; or
- an explicit scope amendment that preserves the prior run's stop reason and
  records the changed field.

Changed fields must be named:

- cap;
- time window;
- sort order;
- source surface;
- seed subreddit;
- candidate surface;
- exclusion rule.

`empty_result`, `blocked_result`, and `caps_reached` are valid terminal outcomes.
They must not trigger automatic scope widening, retry escalation, broad crawl,
or source-access escalation.

When widening after a blocked or empty result, the new run or amendment must
state why the prior result did not satisfy the operator's planning need. It must
not mutate the prior run in place.

## Promotion Receipt Ownership

Default owner: **operator-owned Candidate URL Intake promotion receipt**.

The operator may promote one or more candidate URLs only by writing a promotion
receipt that records:

- exact promoted URL;
- originating `run_id`;
- candidate row pointer;
- reason for promotion;
- known limitations carried from the originating run's provenance receipt
  (declared caps, `coverage_claim`, and any empty/blocked/capped stop reason);
- selected downstream capture method or method family;
- approved downstream access route if already source-backed;
- Decision Frame or approved capture-unit authority, if present;
- non-promotion of non-selected candidate rows;
- confirmation that Source Capture Armory execution has not happened yet;
- `capture_not_yet_authorized: yes` — the receipt is planning context only and
  is not capture, packet, body/comment/profile, Source Capture Armory, or
  source-access authorization; it confers no access until a Decision Frame or
  approved capture-unit authority accepts the promoted unit.

Data Capture commissioning owns the promoted unit only after a Decision Frame or
approved capture-unit authority accepts it. Before that point, the receipt is
planning context only.

Promotion does not authorize capture, packet generation, body/comment fetch,
source-quality scoring, fixture admission, ECR, Cleaning, Judgment, commercial
use, or broad crawling.

## Listing Provenance Defaults

Visible listing title, visible listing timestamp, and visible listing score
state are allowed by default as provenance-only disambiguation fields.

They must not be used to rank, score, include, exclude, summarize, judge
credibility, infer sentiment, or make source-quality decisions.

If a title or listing label contains sensitive ordinary-person or private
spillover once noticed, omit it or replace it with `omitted_sensitive_listing`.

## Access-Method Default

Default Reddit surface posture for future promoted capture: **old Reddit
first**.

Reddit Candidate URL Intake should normalize and validate candidate URL shapes
against old Reddit listing/thread URL conventions first. New Reddit surfaces are
non-default and require a separate scope amendment or later owner decision.

Current implementation default: Reddit `.json` URLs are blocked for Candidate
URL Intake until a later owner decision accepts a JSON projection contract.
This blocks listing `.json`, search `.json`, thread `.json`, user/profile
`.json`, and any raw JSON persistence or output. The first no-live implementation
surface is old Reddit HTML listing/search projection from static fixtures.
Thread pages are candidate URL outputs only and must not be fetched as input
inside Candidate URL Intake.

The default approved downstream access route for promoted Reddit capture is:

`cloakbrowser_primary_anti_blocking`.

This records the already source-backed posture that CloakBrowser is the approved
primary anti-blocking route and residential/rotating proxies are not blanket
stop conditions for bounded pre-commercial Reddit capture.

This lane does not repeat CloakBrowser/proxy setup and does not treat setup as
the blocker for no-live-access scoping. It also does not make Candidate URL
Intake invoke CloakBrowser, reconfigure proxies, fetch source bodies, emit
Source Capture Packets, or claim the current CloakBrowser runner implements
Reddit discovery/consolidation or proxy/session behavior.

If live access is attempted later, the implementing lane must separately bind
the current source-access authorization, already-approved downstream access
substrate, runner capability, secrets policy, and validation gates.

## Implementation-Scoping Gate

After owner acceptance of this default policy and of the parent Candidate URL
Intake contract and Reddit Candidate URL Intake architecture that this decision
specializes, no-live-access implementation scoping may proceed for:

- schema or row model for the run envelope and candidate rows;
- old-Reddit-first URL normalization and validation using static examples;
- old Reddit HTML listing/search projection using static fixtures, with raw
  HTML transient only and no raw HTML or parser output persisted;
- `.json` URL refusal for all Reddit intake input surfaces;
- local file output shape;
- validation that no body/comment/profile/packet fields exist;
- validation that caps, stop reasons, and non-claims are required;
- validation that same-run traversal and auto-promotion are impossible in the
  scoped design.

Still not authorized by this artifact:

- live Reddit access;
- dependency installation;
- CloakBrowser/proxy invocation, reconfiguration, or new setup in this lane;
- browser/API/archive/parser runner dispatch;
- Source Capture Packet generation;
- storage, scheduler, dashboard, deployment, or production runtime;
- ECR, Cleaning, Judgment, fixture admission, source-quality scoring, or
  commercial Reddit use.

## Success Signals

This default policy is complete enough for owner review when a future CA can
answer without inventing policy:

- which `cap_type` is default;
- which numeric caps apply to `probe`, `working_batch`, and
  `high_recall_pass`;
- which surfaces are default-on;
- which surfaces require explicit allowlisting;
- whether outbound links are default-on or opt-in;
- whether monitored runs are default-allowed before a Decision Frame;
- how continuation or widening must be recorded;
- who owns the promotion receipt;
- whether listing title/timestamp/score-state may be recorded;
- whether implementation scoping may proceed after owner acceptance;
- what remains explicitly unauthorized.

Hard success signal: implementation scoping can proceed after owner acceptance
without choosing caps, default surfaces, outbound posture, monitoring posture,
continuation semantics, or promotion ownership.

## Non-Claims

This artifact is not validation, readiness, owner acceptance, source-access
boundary amendment, legal sufficiency, rights clearance, implementation
authorization, live Reddit authorization, Source Capture Armory authorization,
Source Capture Packet generation, Data Capture handoff, ECR design, Cleaning
design, Judgment design, fixture admission, source-quality scoring, buyer proof,
commercial Reddit authorization, storage authorization, dashboard authorization,
scheduler authorization, deployment authorization, production-runtime
authorization, commit authorization, push authorization, or PR authorization.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "Orca now has a recommended default-policy decision for bounded Reddit Candidate URL Intake: probe/working_batch/high_recall caps, default candidate surfaces including capped default-on cross-post and related-subreddit candidate surfaces, old-Reddit-first URL posture, Reddit `.json` intake blocked for now, transient old Reddit HTML listing/search projection from static fixtures, outbound opt-in, monitored-run default-off posture, continuation/widening rules, operator-owned promotion receipt with limitations and non-authorization fields, listing-provenance defaults, downstream CloakBrowser/proxy setup not repeated in this lane, and a no-live-access implementation-scoping gate after owner acceptance of the parent contract, Reddit architecture, and default policy."
  trigger: product_doctrine
  related_triggers:
    - architecture_doctrine
    - output_authority
    - lifecycle_boundary
  controlling_sources_updated:
    - "docs/decisions/data_capture_spine_reddit_candidate_url_intake_default_policy_decision_v0.md"
    - "docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md"
    - "docs/workflows/data_capture_spine_consolidation_map_v0.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/decision-routing.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - ".agents/workflow-overlay/retrieval-metadata.md"
    - ".agents/workflow-overlay/artifact-roles.md"
    - "docs/workflows/orca_repo_map_v0.md"
    - "docs/workflows/data_capture_spine_consolidation_map_v0.md"
    - "docs/product/data_capture_spine_candidate_url_intake_contract_v0.md"
    - "docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md"
    - "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
    - "docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md"
  intentionally_not_updated:
    - path: "docs/workflows/orca_repo_map_v0.md"
      reason: "The top-level repo map already routes Reddit Candidate URL Intake through the Data Capture sub-map and carries the CloakBrowser/proxy allowance quick route. Default-policy detail belongs in the Data Capture sub-map."
    - path: "docs/product/data_capture_spine_candidate_url_intake_contract_v0.md"
      reason: "The parent contract intentionally leaves source-family numeric caps and default surfaces to source-specific owner policy."
    - path: "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
      reason: "Source-access tooling authorization did not change; this decision only records Candidate URL Intake defaults."
  stale_language_search: "rg -n \"default numeric caps|Which candidate surfaces|monitored Reddit scopes|Who owns the promotion receipt|visible listing title|default policy|high_recall_pass|outbound links are default-off|operator-owned Candidate URL Intake promotion receipt|default candidate_surface_allowlist|capture_not_yet_authorized|known limitations carried|parent Candidate URL Intake contract|After owner acceptance of this default policy, no-live-access|old Reddit first|old-Reddit-first|\\.json|HTML listing/search projection|raw HTML|parser output|new CloakBrowser or proxy setup|proxy setup\" docs/decisions/data_capture_spine_reddit_candidate_url_intake_default_policy_decision_v0.md docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md docs/workflows/data_capture_spine_consolidation_map_v0.md"
  stale_language_search_result: "Executed 2026-06-07 after the `.json` hard-block / transient old Reddit HTML projection patch. Hits were the adjudicated default-policy decision, the Reddit architecture, and the Data Capture sub-map route/summary. The checked surfaces did not retain the old unresolved implementation-scoping gate, did not present default-on discovery surfaces as uncapped, did not leave the promotion receipt without the known-limitations and `capture_not_yet_authorized` fields, did not treat CloakBrowser/proxy setup as the blocker for no-live-access scoping, and now carry Reddit `.json` intake as blocked with old Reddit HTML listing/search projection limited to static/no-live fixtures unless separately authorized."
  non_claims:
    - "not validation"
    - "not readiness"
    - "not owner acceptance"
    - "not source-access boundary amendment"
    - "not implementation authorization"
    - "not live Reddit authorization"
    - "not Source Capture Packet generation"
    - "not broad crawling, storage, dashboard, scheduler, deployment, production runtime, ECR, Cleaning, Judgment, fixture admission, source-quality scoring, or commercial authorization"
```
