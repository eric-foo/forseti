# Data Capture Spine Source-Access Tooling Build Authorization v0

```yaml
retrieval_header_version: 1
artifact_role: Product decision
scope: Owner authorization for bounded Data Capture source-access tooling builds — first tranche (capture core + HTTP/media/archive/honest-browser adapters), second tranche (Reddit official API adapter and additional owner-named source adapters), third tranche (anti-blocking), and selected anti-blocking backend/order — after the first pressure-test foundation closeout.
use_when:
  - Checking whether Data Capture source-access tooling builds are now allowed.
  - Scoping or implementing the bounded local source-access/capture-support tools.
  - Distinguishing authorized first/second/third-tranche build scope from commercial fetch, broad crawling, storage, dashboard, deployment, production runtime, or downstream-spine work.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_capture_toolbox/README.md
  - forseti/product/spines/capture/core/contracts/source_access_boundary/data_capture_source_access_method_plan_v0.md
  - forseti/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_closeout_synthesis_v0.md
  - docs/decisions/data_capture_spine_source_observability_requirements_boundary_decision_v0.md
stale_if:
  - A later owner decision supersedes the authorized build scope, selected anti-blocking backend, or Reddit pre-commercial ordering.
  - Current old Reddit Direct HTTP exact-thread capture stops working as the operator default.
  - The source-access boundary decision materially changes hard stops or disclosability requirements.
  - The Data Capture obligation contract, Data Capture/Cleaning/Judgment boundary, or source-access method plan materially changes source-acquisition obligations.
  - First-tranche implementation exposes an access, fidelity, provenance, rights, or boundary issue that cannot be represented by the authorized packet/adapter surface.
```

## Status And Decision

Status: `AUTHORIZED_BOUNDED_SOURCE_ACCESS_TOOLING_BUILD_V0`.

Owner decision:
`AUTHORIZE_BOUNDED_SOURCE_ACCESS_TOOLING_BUILD_FIRST_TRANCHE`.

Data Capture source-access tooling builds are now allowed inside the bounded
first tranche below. This decision supersedes prior "not build tools now" and
`defer_until_separate_owner_authorization` language for this first tranche only.

This is not blanket authorization for every source-access method named in the
method plan. The authorization is deliberately narrow enough that implementation
can start without silently selecting high-risk adapters, downstream schema, or
production infrastructure.

### Second-Tranche Amendment (2026-06-04)

Owner decision: `AUTHORIZE_SOURCE_ACCESS_TOOLING_BUILD_SECOND_TRANCHE`.

The owner authorized a second tranche of source-access adapter builds so the
Source Capture Armory can reliably capture canonical high-information sources per
discipline (for example Wall Street Oasis for finance, Reddit broadly) and "pull
the trigger when needed." The authorized second-tranche surface is in
`## Authorized Second-Tranche Build Surface` below. Scrapy/broad crawlers,
anti-detect browsers, residential/rotating proxies, commercial fetch services,
SERP APIs, and storage/dashboard/scheduler/deployment/production-runtime surfaces
remain deferred. The source-access boundary and its hard stops are unchanged.

### Third-Tranche Amendment (2026-06-05)

Owner decision: `AUTHORIZE_SOURCE_ACCESS_TOOLING_BUILD_THIRD_TRANCHE_ANTI_BLOCKING`.

The owner authorized a third tranche covering the anti-blocking techniques the
source-access boundary already permits, for the current pre-commercial / free
phase: anti-detect / cloaked browser configuration, residential or rotating
proxy integration, and in-browser JS-challenge handling — used only to reach
public / discoverable source material inside the unchanged boundary. Rationale:
while Orca is on free / unsanctioned access tiers, anti-blocking is the in-bounds
way to reach public sources without being rate-throttled or IP-blocked. This is a
deliberate, disclosable, owner-accepted-risk posture (ToS / reputational /
litigation risk per the boundary decision; real legal counsel advisable before
commercializing).

Re-tighten trigger: when Orca goes commercial / enterprise on a source, it moves
that source to the sanctioned path (for Reddit, the enterprise API tier) and
stops relying on anti-blocking for it. This tranche is the pre-commercial bridge,
not the commercial-scale method.

Still deferred (need a separate owner authorization): Scrapy / broad
crawler-spider frameworks, commercial scraping / fetch-service integration,
standalone CAPTCHA-solving services (paid solver services, distinct from the
in-browser JS-challenge handling authorized here), SERP / discovery APIs, and
persistent storage / database / dashboard / queue / scheduler / deployment /
production-runtime surfaces. The source-access boundary and its hard stops are
unchanged.

### Anti-Blocking Backend And Reddit Ordering Amendment (2026-06-05)

Owner decision: `SELECT_CLOAKBROWSER_PRIMARY_ANTI_BLOCKING_BACKEND`.

For the authorized third-tranche anti-blocking surface, Orca selects
**CloakBrowser** as the primary backend for the next anti-blocking browser
implementation lane. Patchright remains an optional lower-change compatibility
fallback, not the default first probe, because the armory's job is reliable
capture on already-known actively blocking public/discoverable sources, not
minimizing a failed experiment's integration cost.

For Reddit during the current pre-commercial / personal-project phase, Orca uses
this source-specific order:

1. exact old Reddit Direct HTTP first for supplied thread URLs when current old
   Reddit HTML is the capture target and the bounded batch runner accepts the
   URL;
2. CloakBrowser anti-blocking browser capture for one supplied URL when Direct
   HTTP is unsuitable, blocked, or browser-visible anti-blocking capture is
   explicitly needed; CloakBrowser remains the primary anti-blocking backend;
3. low-volume bounded capture over source sets that are subreddit-bounded,
   thematic, or thread-family scoped;
4. archive capture for historical thread posture or when live capture is not
   necessary or fails visibly.

The Reddit bound is **not URL-only**. A bounded capture unit may be a subreddit,
theme, query, thread family, or small monitored thread set when the operator
names the boundary and records it in provenance. This does not authorize broad
crawling, site-wide walking, generic subreddit harvesting, production monitoring,
or volume escalation. The capture must remain low-volume and purpose-bounded,
with method provenance recorded plainly.

Cold Reddit `.json` endpoints are not a primary pre-commercial capture spine.
Current spot checks from Reddit's own help/dev surfaces and live developer
reports show that OAuth/login credentials are expected for Data API use and
anonymous `.json` reads are seeing 403/network-security failures. Orca's bounded
2026-06-08 probes also saw cold direct `.json`, cold browser `.json`, and cold
CloakBrowser+proxy `.json` fail with network-security blocks.

The useful bounded JSON route is warm same-context JSON: load the exact old
Reddit HTML thread first in CloakBrowser, confirm the page is not blocked, then
fetch the same thread's `.json` URL inside that same browser context. Treat that
as a structured enrichment path over the same supplied thread, not as standalone
cold JSON access, source discovery, crawling, monitoring, storage, or commercial
API use. The old Reddit HTML surface remains the preferred provenance surface
for this tranche. Direct HTTP is the current exact-thread operator default for
that surface; CloakBrowser is the anti-blocking/browser-visible route, not a
reason to skip a working Direct HTTP capture.

BeautifulSoup-style HTML parsing is allowed as a parser over already retrieved
old Reddit HTML or archived HTML. It is not an access method and does not solve
blocking, login, JavaScript, rate-limit, or anti-bot posture by itself.

When Orca goes commercial / enterprise on Reddit or another source, the source
moves to the sanctioned or commercial path for that source. For Reddit, that is
the commercial / enterprise API or data-licensing route. Anti-blocking remains a
pre-commercial bridge, not the commercial-scale method.

## Source Basis

Decision inputs:

- Current owner instruction: "first, update docs to state building out tools are okay".
- `docs/product/data_capture_spine_pressure_test_closeout_synthesis_v0.md`.
- `docs/product/data_capture_source_access_method_plan_v0.md`.
- `docs/decisions/data_capture_spine_source_observability_requirements_boundary_decision_v0.md`.
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`.
- `.agents/workflow-overlay/source-loading.md`.

The pressure-test foundation is good enough to stop treating all source-access
tooling as premature. The strongest repeated pressure is not a need for
Judgment, Cleaning, or ECR design; it is source observability, source-language
fidelity, archive/media preservation, and inspectable acquisition receipts.

## Authorized First-Tranche Build Surface

The first tranche may build local source-access/capture-support tooling for:

1. **Source Capture Packet core and CLI**
   - create a local packet for one requested source or small source set;
   - preserve raw/source-visible artifacts where available;
   - record locator, acquisition time, cutoff posture, access posture, hashes,
     warnings, and limitation notes;
   - emit a human-inspectable packet receipt.

2. **Direct HTTP fetch adapter**
   - retrieve public or discoverable pages when normal HTTP access works;
   - preserve response body, headers useful for provenance, final URL, status,
     and hash;
   - record access failures visibly rather than hiding them.

3. **Media / asset preservation adapter**
   - fetch and preserve source-linked images, galleries, screenshots, or other
     media artifacts when they carry source meaning and remain inside the
     source-access boundary;
   - record pointer-only or unavailable media explicitly when preservation fails.

4. **Archive.org availability and snapshot adapter**
   - query archive availability/CDX metadata;
   - retrieve snapshot body content when accessible through ordinary HTTP/browser
     routes;
   - distinguish archive availability from archive-body retrieval.

5. **Honest browser snapshot adapter**
   - use a normal browser/headless-browser path for pages that require
     JavaScript rendering or logged-in/entitled visible access;
   - preserve visible HTML/text/screenshot artifacts and receipt metadata;
   - avoid anti-detect, proxy rotation, or no-entitlement bypass in this tranche.

These tools should produce capture-support artifacts. They must not decide
credibility, usefulness, inclusion, exclusion, discounting, Signal Use, Decision
Strength, Action Ceiling, buyer proof, or commercial meaning.

## Authorized Second-Tranche Build Surface

The second tranche (owner-authorized 2026-06-04) may build, against the same
Source Capture Packet/adapter shape and the cross-adapter contract decided by the
Source Capture Armory architecture lane:

6. **Reddit official API adapter** (first / reference adapter)
   - registered-app OAuth2 read access to public subreddit posts, comments, and
     full comment trees through the official Reddit API;
   - return verbatim post/comment text into the packet shape with per-thread
     slice state, locator, cutoff posture, access posture, hashes, and limitation
     notes;
   - record rate-limit, deleted-row, and not-retrieved states visibly.

7. **Additional owner-named source adapters**
   - build the next high-value source adapter(s) the owner names (for example a
     Wall Street Oasis path through the existing honest/authenticated browser
     snapshot adapter, tested live), against the same packet/adapter contract and
     an agent-facing source-class -> adapter selection surface.

8. **Cross-adapter contract and agent-facing selection surface**
   - the shared adapter interface, credential/secret handling pattern, and the
     agent-facing source-class -> adapter selection map, as decided by the Source
     Capture Armory architecture lane (not pre-decided here).

Invariant for any second-tranche adapter that needs authentication or API
credentials: credentials, tokens, cookies, and storage-state never enter the
packet and are never copied, hashed, printed, or preserved there; they live in
local ignored config only. This restates the source-access hard stops and the
fixture/retention/sensitivity contamination stop; it is not optional.

Like the first tranche, these tools produce capture-support artifacts only. They
must not decide credibility, usefulness, inclusion, exclusion, discounting,
Signal Use, Decision Strength, Action Ceiling, buyer proof, or commercial
meaning. Generated packets remain `scratch` under the fixture/retention/
sensitivity decision unless separately admitted.

## Authorized Third-Tranche Build Surface

The third tranche (owner-authorized 2026-06-05) may build, against the same
Source Capture Packet/adapter shape and hard stops:

9. **CloakBrowser anti-blocking browser adapter** (primary anti-blocking backend)
   - use CloakBrowser as the default anti-blocking / cloaked Chromium route for
     public or discoverable source material that ordinary browser capture is
     expected to miss or fail;
   - preserve visible HTML/text/screenshot artifacts, access posture, bounded
     source-set posture, method provenance, warnings, hashes, and limitation
     notes in the packet shape;
   - support Reddit pre-commercial capture over named subreddit/thematic/thread
     family bounds without requiring each run to start from a single supplied URL;
   - prefer old Reddit HTML capture for Reddit where available, with optional
     BeautifulSoup-style parsing after HTML is retrieved and preserved;
   - keep low-volume capture limits and no-broad-crawling stops visible.

Patchright may be used later as a compatibility fallback or cheaper migration
probe if CloakBrowser introduces a concrete operational blocker. It is not the
primary backend selected by this decision.

CloakBrowser selection does not authorize stolen credentials, raw cookie import,
nonconsensual sessions, no-entitlement gate bypass, obvious private/admin
spillover, broad crawler/spider frameworks, commercial fetch services, standalone
CAPTCHA-solving services, storage/dashboard/scheduler/deployment/production
runtime, or Judgment/ECR/Cleaning behavior.

## Deferred Or Separately Authorized Build Surface

The following remain in-bounds method candidates under the source-access method
plan, but are not authorized for implementation by this decision (first, second,
or third tranche). Reddit API moved to the second tranche. Anti-detect browser,
residential/rotating proxy, and in-browser JS-challenge handling moved to the
third tranche, with CloakBrowser selected as the primary anti-blocking browser
backend.

- Scrapy or other broad crawler/spider frameworks for systematic site-wide URL
  discovery and large-scale walking (a breadth-at-scale / post-sale tool, not a
  fetch-known-URLs tool);
- commercial scraping or fetch-service integration;
- standalone CAPTCHA-solving service integration (paid solver services), as
  distinct from the in-browser JS-challenge handling authorized in the third
  tranche;
- SERP/discovery API integration;
- persistent storage, database, dashboard, queue, scheduler, deployment,
  production crawler, or broad source-system runtime.

If any deferred surface becomes necessary, write a separate owner authorization
that names the adapter, source family, risk posture, and non-claims.

## Boundary Guards

This authorization does not change the source-access boundary. The hard stops
remain:

- no-entitlement gate bypass;
- stolen credentials, stolen cookies, or nonconsensual sessions;
- security exploits, malware, credential stuffing, or obvious cross-account,
  private, admin, or confidential spillover once noticed;
- methods Orca would refuse to disclose internally;
- anything clearly illegal or too morally compromising for Orca to own.

The first tranche may use free/account-created access and legitimately entitled
paid/client/coworker access where it stays within the boundary and records the
access posture visibly.

## Non-Claims

This decision is not validation, readiness, pressure-test discharge, source
adequacy, capture closure, source-of-truth promotion, contract hardening,
source-access boundary amendment, ECR design, Cleaning implementation, Judgment
design, buyer proof, commercial-readiness evidence, API authorization,
commercial-scraper authorization, standalone CAPTCHA-solving-service
authorization, production-runtime authorization, storage authorization,
dashboard authorization, deployment authorization, or legal sufficiency. (The
Third-Tranche Amendment above authorizes anti-detect / proxy / in-browser
JS-challenge builds; those are no longer disclaimed here.)

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "Data Capture source-access tooling is no longer globally deferred: the owner authorized a bounded first-tranche build surface for local Source Capture Packet core, direct HTTP, media/asset preservation, archive availability/body retrieval, and honest browser snapshot support, while leaving API/commercial/anti-detect/proxy/production runtime surfaces separately gated."
  trigger: lifecycle_boundary
  controlling_sources_updated:
    - "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
    - "docs/product/source_capture_toolbox/README.md"
    - "docs/product/data_capture_source_access_method_plan_v0.md"
    - "docs/product/data_capture_spine_pressure_test_closeout_synthesis_v0.md"
    - ".agents/workflow-overlay/source-loading.md"
    - "docs/workflows/orca_repo_map_v0.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - ".agents/workflow-overlay/source-loading.md"
    - "docs/workflows/orca_repo_map_v0.md"
    - "docs/product/source_capture_toolbox/README.md"
    - "docs/product/data_capture_source_access_boundary_decision_v0.md"
    - "docs/product/data_capture_source_access_method_plan_v0.md"
    - "docs/product/data_capture_spine_pressure_test_closeout_synthesis_v0.md"
    - "docs/decisions/data_capture_spine_source_observability_requirements_boundary_decision_v0.md"
    - "docs/decisions/data_capture_spine_source_observability_local_support_implementation_execution_authorization_v0.md"
    - "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
  intentionally_not_updated:
    - path: "AGENTS.md"
      reason: "Top-level rule already permits bounded implementation when a current turn or accepted handoff explicitly authorizes it."
    - path: ".agents/workflow-overlay/source-of-truth.md"
      reason: "Source hierarchy and propagation mechanics did not change; this decision uses the existing lifecycle_boundary trigger."
    - path: "docs/product/data_capture_source_access_boundary_decision_v0.md"
      reason: "Boundary permission and hard stops did not change; only build authority changed."
    - path: "docs/decisions/data_capture_spine_source_observability_requirements_boundary_decision_v0.md"
      reason: "The requirements-boundary decision remains accurate for RQ classification and already says implementation needs separate owner authorization; this later decision supplies that authorization for a different first-tranche source-access scope."
    - path: "docs/decisions/data_capture_spine_source_observability_local_support_implementation_execution_authorization_v0.md"
      reason: "The prior local-helper execution authorization remains accurate for that helper and does not need to become source-access build authority."
    - path: "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
      reason: "The obligation contract already allows runtime work when the current turn or accepted handoff authorizes it; this decision does not amend Capture obligations or harden the contract."
  stale_language_search: "rg -n \"not build tools now|defer_until_separate_owner_authorization|No build, no install, no runtime authorized|No build authorization|build_authorization: NOT GRANTED|source-access implementation, runtime/tooling\" docs/product/data_capture_source_access_method_plan_v0.md docs/product/data_capture_spine_pressure_test_closeout_synthesis_v0.md .agents/workflow-overlay/source-loading.md docs/workflows/orca_repo_map_v0.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not source-access boundary amendment"
    - "not API, commercial-scraper, anti-detect, proxy, or production-runtime authorization"
    - "not ECR, Cleaning, or Judgment design"
```

## Direction Change Propagation - Second-Tranche Amendment

```yaml
direction_change_propagation:
  doctrine_changed: "The owner authorized a bounded second tranche of source-access adapter builds - Reddit official API adapter (reference) plus additional owner-named source adapters and the cross-adapter contract/selection surface - while Scrapy/broad crawlers, anti-detect, proxies, commercial fetch, SERP, and storage/dashboard/scheduler/deployment/production-runtime remain deferred and the source-access boundary is unchanged."
  trigger: lifecycle_boundary
  related_triggers:
    - output_authority
  controlling_sources_updated:
    - "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - ".agents/workflow-overlay/source-loading.md"
    - "docs/product/source_capture_toolbox/README.md"
    - "docs/product/data_capture_source_access_method_plan_v0.md"
    - "docs/product/data_capture_source_access_boundary_decision_v0.md"
    - "docs/workflows/orca_repo_map_v0.md"
  intentionally_not_updated:
    - path: "docs/product/data_capture_source_access_boundary_decision_v0.md"
      reason: "Boundary permission and hard stops are unchanged; Reddit API and the deferred methods were already in-bounds. Only build authority changed."
    - path: ".agents/workflow-overlay/source-loading.md"
      reason: "Its source-access paragraph accurately describes the first-tranche authorization and routes agents to this authority doc for current build scope; the second tranche is additive in this same doc, not a live contradiction. Optional follow-on cross-reference refresh."
    - path: "docs/product/source_capture_toolbox/README.md"
      reason: "Build-order step 9 and the deferred-gaps list treat Reddit API as 'decide separately'; this decision is that separate decision and routes here. README refresh left as a bounded follow-on to avoid churn on an already display-name-dirty file."
    - path: "docs/product/data_capture_source_access_method_plan_v0.md"
      reason: "Its Step-3 'evaluate after first-tranche dry use' and build catalogue already route build authority here; the second tranche is that evaluation outcome for Reddit and is additive."
    - path: "AGENTS.md"
      reason: "Already permits bounded implementation when the current turn authorizes it."
    - path: ".agents/workflow-overlay/source-of-truth.md"
      reason: "Source hierarchy and propagation mechanics unchanged; existing lifecycle_boundary trigger used."
  stale_language_search: "rg -n \"Reddit API.*deferred|does not cover Reddit API|Reddit API registration.*unless|decide separately whether|Reddit API.*separately gated\" .agents/workflow-overlay/source-loading.md docs/product/source_capture_toolbox/README.md docs/product/data_capture_source_access_method_plan_v0.md docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not source-access boundary amendment"
    - "not Scrapy, anti-detect, proxy, commercial-fetch, SERP, storage, or production-runtime authorization"
    - "not ECR, Cleaning, or Judgment design"
    - "not legal sufficiency"
```

## Direction Change Propagation - Third-Tranche Amendment

```yaml
direction_change_propagation:
  doctrine_changed: "The owner authorized a bounded third tranche of source-access tooling - anti-detect/cloaked browser configuration, residential/rotating proxy integration, and in-browser JS-challenge handling - for the pre-commercial free phase, to reach public/discoverable sources inside the unchanged boundary; standalone CAPTCHA-solving services, commercial fetch, Scrapy/broad crawlers, SERP, and storage/dashboard/scheduler/deployment/production-runtime remain deferred."
  trigger: lifecycle_boundary
  related_triggers:
    - product_doctrine
  controlling_sources_updated:
    - "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
    - "orca-harness/docs/adapter_author_contract.md"
  downstream_surfaces_checked:
    - ".agents/workflow-overlay/source-loading.md"
    - ".agents/workflow-overlay/safety-rules.md"
    - "docs/product/data_capture_source_access_boundary_decision_v0.md"
    - "docs/product/data_capture_source_access_method_plan_v0.md"
    - "docs/product/source_capture_toolbox/README.md"
    - "docs/workflows/orca_repo_map_v0.md"
  intentionally_not_updated:
    - path: ".agents/workflow-overlay/source-loading.md"
      reason: "Its current-build-scope paragraph still says the authorization does not cover anti-detect browsers / proxies (and Reddit API). Stale echo of build scope, not the controlling authority; flagged for an immediate bounded follow-on refresh, same treatment the second-tranche receipt gave this file."
    - path: ".agents/workflow-overlay/safety-rules.md"
      reason: "Line-8 bounded-scope caution lists anti-detect/proxies among separate gates to preserve; now build-authorized. Bounded follow-on refresh; the rule itself (bounded implementation is not blanket runtime authority) is unchanged."
    - path: "docs/product/data_capture_source_access_method_plan_v0.md"
      reason: "Build catalogue + sequencing already route build authority to this decision; the third tranche is additive. Cross-reference refresh is a bounded follow-on."
    - path: "docs/product/source_capture_toolbox/README.md"
      reason: "Armory README lists anti-detect/proxy as separately gated in its build-order and deferred-gaps; refresh left as a bounded follow-on, same treatment as the second-tranche receipt, to avoid churn on an already display-name-dirty file."
    - path: "docs/product/data_capture_source_access_boundary_decision_v0.md"
      reason: "Boundary already permits anti-detect/proxy/JS-challenge with owner-accepted risk; only build authority changed, not the boundary."
    - path: "docs/workflows/orca_repo_map_v0.md"
      reason: "Repo map indexes this decision at a path level and does not enumerate per-tranche build scope."
  stale_language_search: "rg -ni 'anti-detect|rotating proxy|residential proxy|proxy integration|proxy authorization|avoid anti-detect' across the controlling + downstream paths above"
  stale_language_search_result: "Run 2026-06-05. Controlling surfaces (this decision's third tranche + deferred list + non-claims; the contract not-in-scope line) updated to mark anti-detect/proxy/JS-challenge as build-authorized. Remaining live hits in source-loading + safety-rules are stale build-scope echoes flagged for an immediate bounded follow-on; method-plan + toolbox README echoes are additive follow-ons; other hits are historical DCP receipts/non-claims preserved as records, and the boundary decision where these methods were already in-bounds."
  non_claims:
    - "not validation"
    - "not readiness"
    - "not source-access boundary amendment"
    - "not commercial-fetch, Scrapy, SERP, standalone-CAPTCHA-service, storage, or production-runtime authorization"
    - "not legal sufficiency"
    - "not Reddit live-run authorization"
```

## Direction Change Propagation - CloakBrowser And Reddit Pre-Commercial Order

```yaml
direction_change_propagation:
  doctrine_changed: "The owner selected CloakBrowser as Orca's primary third-tranche anti-blocking browser backend and set Reddit's pre-commercial order to anti-blocking browser first, old Reddit HTML where available, low-volume bounded subreddit/thematic/thread-family capture, then archive capture, with anonymous `.json` opportunistic only, BeautifulSoup parser-only, and commercial Reddit use moving to the sanctioned commercial / enterprise API or data-licensing path."
  trigger: product_doctrine
  related_triggers:
    - lifecycle_boundary
    - architecture_doctrine
  controlling_sources_updated:
    - "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
    - "docs/product/data_capture_source_access_method_plan_v0.md"
    - "docs/product/source_capture_toolbox/README.md"
    - ".agents/workflow-overlay/source-loading.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - ".agents/workflow-overlay/safety-rules.md"
    - "docs/workflows/orca_repo_map_v0.md"
    - "docs/workflows/data_capture_spine_consolidation_map_v0.md"
    - "orca-harness/docs/source_capture_agent_runbook.md"
    - "orca-harness/docs/adapter_author_contract.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - "docs/product/data_capture_source_access_boundary_decision_v0.md"
    - "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
    - "orca-harness/source_capture/adapters/"
  intentionally_not_updated:
    - path: "AGENTS.md"
      reason: "Top-level project instructions already permit bounded implementation only under current-turn or accepted-decision authority and do not encode source-specific ordering."
    - path: "docs/product/data_capture_source_access_boundary_decision_v0.md"
      reason: "The boundary already permits disclosable anti-blocking techniques and hard stops are unchanged; this patch selects backend/order, not boundary permission."
    - path: "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
      reason: "Capture obligations and forbidden Capture outputs did not change."
    - path: "orca-harness/source_capture/adapters/"
      reason: "No implementation was performed in this docs-only owner-decision pass; runbook now states CloakBrowser is authorized but not implemented in current runners."
  stale_language_search: "rg -n \"Reddit official API.*cleanest|human-led/browser-visible capture by default pre-sale|human-led browser capture.*primary default|API access is not the default pre-sale route|anti-detect.*remain separately gated|does not cover Reddit API|anonymous `.json`.*primary|BeautifulSoup.*access method|old Reddit|Data Capture Spine entry map|data_capture_spine_consolidation_map\" docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md docs/product/data_capture_source_access_method_plan_v0.md docs/product/source_capture_toolbox/README.md .agents/workflow-overlay/source-loading.md .agents/workflow-overlay/source-of-truth.md docs/workflows/orca_repo_map_v0.md docs/workflows/data_capture_spine_consolidation_map_v0.md orca-harness/docs/source_capture_agent_runbook.md orca-harness/docs/adapter_author_contract.md"
  stale_language_search_result: "Executed 2026-06-05 after the old Reddit / `.json` / BeautifulSoup and Data Capture Spine map patch. Remaining hits are current old Reddit preference, `.json` opportunistic-only posture, BeautifulSoup parser-only posture, Data Capture Spine map pointers, the honest-browser runner's one-supplied-URL scope, current runbook notes that CloakBrowser is authorized but not implemented there, and historical DCP receipt text. No live routing surface still makes Reddit API or anonymous `.json` the default pre-commercial route, treats BeautifulSoup as an access method, or treats anti-blocking/proxy as deferred by current authority."
  non_claims:
    - "not validation"
    - "not readiness"
    - "not source-access boundary amendment"
    - "not legal sufficiency"
    - "not implementation execution"
    - "not CloakBrowser installed"
    - "not Reddit live-run authorization"
    - "not commercial fetch, broad crawling, storage, dashboard, deployment, or production-runtime authorization"
    - "not ECR, Cleaning, or Judgment design"
```
