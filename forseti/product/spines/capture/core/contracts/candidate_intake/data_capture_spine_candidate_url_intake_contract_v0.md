# Data Capture Spine Candidate URL Intake Contract v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture contract
scope: Defines Capture Spine Candidate URL Intake as the generic pre-promotion lane for bounded candidate source locators, before Source Capture Armory packet capture or Data Capture handoff.
use_when:
  - Deciding whether a source-discovery or crawler-shaped activity belongs in Candidate URL Intake.
  - Defining candidate locator rows, run envelopes, provenance receipts, stop reasons, and promotion gates.
  - Preventing candidate intake from becoming broad crawling, source capture, ECR, Cleaning, Judgment, fixture admission, or source-quality scoring.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
  - forseti/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - forseti/product/spines/capture/core/contracts/source_access_boundary/data_capture_source_access_boundary_decision_v0.md
  - forseti/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md
stale_if:
  - Data Capture commissioned-capture scope or Decision Frame requirements change.
  - Source-access discovery/materiality doctrine changes.
  - Candidate URL Intake becomes owned by a broader Candidate Signal Intake or Corpus Intake contract.
  - Source Capture Armory packet lifecycle, runner authority, or Source Capture Packet (CapturePacket) output rules move to a new owner.
```

## Status

Status: `TARGET_RECOMMENDED`.

This is the parent architecture contract for **Capture Spine Candidate URL
Intake**.

Candidate URL Intake is the bounded, pre-promotion lane for collecting source
locators and method provenance before any approved capture unit exists. It may
support operator-facing names such as `crawler`, `finder`, `scout`, or
`intake`, but durable Orca routing must treat the lane as candidate intake, not
capture, scraping, corpus construction, or Data Capture.

Implementation authorized by this artifact: no.

Runtime source access, dependency installation, runner dispatch, Source Capture
Packet generation, storage, queueing, dashboarding, scheduling, deployment,
production monitoring, ECR, Cleaning, Judgment, fixture admission,
source-quality scoring, commercial source acquisition, or Data Capture handoff
authorized by this artifact: no.

## Source Context Status

`SOURCE_CONTEXT_READY` for the docs-only parent contract and routing patch. This
artifact does not claim validation, implementation readiness, source freshness
for every adjacent file, clean-tree state, legal sufficiency, or owner
acceptance.

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom Candidate URL Intake / Data Capture / Source Capture Armory pack
  edit_permission: docs-write
  target_scope:
    - docs/product/data_capture_spine_candidate_url_intake_contract_v0.md
    - docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
  dirty_state_checked: yes
  blocked_if_missing: none for this docs-only contract write
```

Primary grounding sources:

- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/decision-routing.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/retrieval-metadata.md`
- `docs/workflows/data_capture_spine_consolidation_map_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
- `docs/product/data_capture_source_access_boundary_decision_v0.md`
- `docs/product/data_capture_source_access_method_plan_v0.md`
- `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md`
- `forseti/product/spines/capture/core/source_capture_toolbox/README.md`
- `forseti/product/spines/capture/core/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md`
- `docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md`

## Cynefin And Fused Routing

Smallest complete outcome: create the generic Candidate URL Intake foundation
and patch the Reddit specialization and Data Capture sub-map to route through
it, without implementation.

Regime: complicated, with a complex edge around owner-policy defaults.

Why: existing Orca sources define commissioned Data Capture, source-access
materiality, Armory packet capture, and Reddit candidate/scouting gaps; the
missing layer is the parent candidate-intake contract.

Decomposition: layer-based. The parent contract owns generic lane shape, schemas,
promotion, caps, and hard stops; source-specific artifacts own surface-specific
fields and examples.

Current bottleneck: candidate rows must remain inert planning context until a
separate promotion gate binds a locator to an approved capture unit.

Riskiest assumption: a bounded candidate locator row can be useful without being
treated as source capture, corpus capture, or evidence-grade Data Capture input.

Stop or pivot condition: if a proposed lane must fetch source bodies, preserve
rendered pages, invoke a runner, rank source quality, admit fixtures, or hand
off to ECR/Cleaning/Judgment, it is no longer Candidate URL Intake.

Allowed next move: docs-only contract use by source-specific candidate-intake
artifacts.

Disallowed next move: runtime implementation, live source access, broad crawler
build, Source Capture Armory dispatch, Source Capture Packet output, or direct
Data Capture handoff.

Fused lane result for this turn: `/fused` is narrowed to non-code
artifact-writing. Implementation scoping blocks runtime implementation because
this is doctrine-bearing source architecture, not an authorized build. Spec
writing is satisfied by this contract body. Micro-decision locking freezes the
patch boundary: create the parent contract, patch the Reddit specialization and
sub-map only, do not choose numeric caps or default surfaces, and do not touch
Armory implementation docs.

## Contract Rule

Candidate URL Intake may produce candidate locators and provenance only.

A candidate locator is not:

- source material;
- a Source Capture Packet;
- a capture unit;
- Data Capture handoff input;
- ECR-ready evidence;
- Cleaning input;
- Judgment input;
- fixture-admitted material;
- source-quality output;
- a commercial-use claim.

A candidate locator can become eligible for capture only through a separate
promotion gate. Promotion does not capture the source. It records that one
locator has been selected for a later authorized capture path and that
non-selected candidates remain inert planning context.

## Downstream Access-Method Posture

Candidate URL Intake may record the approved downstream access route for a
source-family specialization, but recording that route is not execution.

If a source-specific owner artifact or accepted source-access decision names a
primary access method, Candidate URL Intake may carry that method as
`approved_downstream_access_route_or_none` in run-level provenance and promotion
receipts. The field is planning context only. It must not cause the intake lane
to invoke a browser, proxy, API, archive, parser runner, packet runner, or
source capture tool.

Candidate URL Intake may use a source-family-specific **transient projection
helper** only when the source-family artifact explicitly allows it. Projection
means converting an already-declared listing/search surface representation into
candidate rows in memory, then discarding the source representation. Projection
must not persist raw source payloads, parser output, screenshots, rendered DOM,
source body text, comments, profiles, secrets, packets, rankings, or scores.

For Reddit, the current downstream posture is source-backed: CloakBrowser is the
approved primary anti-blocking browser route for bounded pre-commercial Reddit
capture, and residential or rotating proxies are not blanket stop conditions
inside the pre-commercial/free anti-blocking posture. The current anonymous
CloakBrowser v0 runner remains one supplied URL and does not implement Reddit
discovery/consolidation or proxy/session behavior by itself.

## Ownership

Owner lane: **Capture Spine Candidate URL Intake**.

Adjacent non-owner lanes:

- Source Capture Armory owns packet-producing capture tools and Source Capture
  Packet lifecycle.
- Data Capture owns commissioned capture after a Decision Frame or approved
  capture unit exists.
- ECR owns evidence-candidate receipt semantics after Data Capture handoff.
- Cleaning owns transformations after capture.
- Judgment owns decision use, confidence, Action Ceiling, Decision Strength, and
  materiality consequences.
- Source-quality support owns source-quality posture over already-bounded source
  units and existing packets, never source discovery or ranking by default.

## Required Run Envelope

A Candidate URL Intake run is invalid unless the envelope is declared before
execution:

- `run_id`;
- `source_family`;
- `declared_topic_theme_query_or_seed`;
- optional `seed_locators`;
- `run_purpose`;
- `non_commercial_posture`;
- `candidate_surface_allowlist`;
- caps for each allowed candidate surface;
- `max_pages_or_result_surfaces`;
- `time_window_or_cutoff_scope`;
- `sort_order_or_surface_order`;
- `exclusions`;
- `method_category`;
- `stop_condition`;
- optional `monitoring_cadence` only with a hard `stop_date`.

The envelope is the boundary. Workers, tools, subagents, and later
continuations inherit it; they do not silently expand it.

## Allowed Outputs

Candidate URL Intake has four generic output types:

1. Candidate source-container row.
2. Candidate source-item locator row.
3. Candidate outbound locator row.
4. Run-level provenance receipt.

Source-specific artifacts may rename these rows for their source family. For
example, Reddit specializes source-container rows as candidate subreddit rows
and source-item locator rows as candidate thread URL rows.

### Candidate Source-Container Row

Use this row when the candidate is a bounded container, community, channel,
board, collection, account-independent listing, or equivalent source surface
that could seed a later bounded run.

Required fields:

- `run_id`;
- `capture_unit_intake_status`: `candidate_or_scouting`;
- `source_family`;
- `candidate_locator_type`: `source_container`;
- `candidate_locator`;
- `candidate_locator_display_name_or_none`;
- `declared_topic_theme_query_or_seed`;
- `source_surface`;
- `query_or_listing_path`;
- `sort_order_or_surface_order`;
- `time_window_or_cutoff_scope`;
- `enumeration_timestamp`;
- `method_category`;
- `exclusion_receipt`;
- `visible_container_volume_or_activity_or_none`;
- `visible_volume_signal_absent_reason_or_none`;
- `visible_stop_reason_if_any`;
- `allowed_downstream_use`: default `planning_only`.

Visible container volume or activity is optional provenance only. It may be
recorded when the declared source surface visibly exposes a container-level
count or activity label, such as subscribers, members, followers, or active
users. It must not be inferred from rank, row count, memory, hidden metadata,
account chrome, or unrelated navigation. If the source surface does not expose
volume or activity, record a volume-absent reason or omit the field.

### Candidate Source-Item Locator Row

Use this row when the candidate is a bounded source item such as a thread, post,
page, article, listing entry, document URL, or equivalent locator that could be
promoted later.

Required fields:

- `run_id`;
- `capture_unit_intake_status`: `candidate_or_scouting`;
- `source_family`;
- `candidate_locator_type`: `source_item`;
- `candidate_locator`;
- `candidate_container_locator_or_none`;
- `visible_listing_title_or_none`;
- `visible_listing_timestamp_or_none`;
- `visible_listing_state_or_none`;
- `declared_topic_theme_query_or_seed`;
- `source_surface`;
- `query_or_listing_path`;
- `sort_order_or_surface_order`;
- `time_window_or_cutoff_scope`;
- `enumeration_timestamp`;
- `method_category`;
- `exclusion_receipt`;
- `visible_stop_reason_if_any`;
- `allowed_downstream_use`: default `planning_only`.

### Candidate Outbound Locator Row

Use this row when a candidate item exposes a locator that leaves the current
source family. Outbound candidates may be useful, but they must not be fetched
inside the current source-family intake run.

Required fields:

- `run_id`;
- `capture_unit_intake_status`: `candidate_or_scouting`;
- `source_family`;
- `candidate_locator_type`: `outbound_locator`;
- `source_item_locator_or_none`;
- `outbound_locator`;
- `visible_listing_anchor_or_context_or_none`;
- `declared_topic_theme_query_or_seed`;
- `source_surface`;
- `query_or_listing_path`;
- `sort_order_or_surface_order`;
- `time_window_or_cutoff_scope`;
- `enumeration_timestamp`;
- `method_category`;
- `exclusion_receipt`;
- `requires_separate_source_family_intake`: `yes`;
- `visible_stop_reason_if_any`;
- `allowed_downstream_use`: default `planning_only`.

Outbound locator rows must not be fetched, rendered, archived, summarized,
packetized, ranked, or scored by Candidate URL Intake.

### Run-Level Provenance Receipt

Required fields:

- `run_id`;
- declared run envelope;
- source family;
- allowed candidate surfaces;
- caps applied;
- exclusions applied;
- source surfaces reached;
- query/listing paths;
- sort order or surface order;
- time window or cutoff scope;
- method category;
- approved downstream access route, if already source-backed;
- enumeration timestamps;
- row counts by type;
- stop reason;
- `cap_type`;
- `coverage_claim`;
- empty-result, blocked-result, or hard-stop state if applicable;
- non-commercial posture;
- non-claims.

## Explicit Non-Outputs

Candidate URL Intake must not output, preserve, derive, or imply:

- source body text;
- comment, reply, or discussion body text;
- user profile data;
- ordinary-person dossier data;
- private, admin, cross-account, or confidential spillover once noticed;
- hidden session state;
- credentials, cookies, browser profiles, storage-state, session sidecars,
  authorization headers, or secrets;
- raw HTML;
- screenshots;
- rendered DOM;
- parser output;
- Source Capture Packets;
- packet lifecycle state;
- capture manifests;
- fixture admission or fixture recommendation;
- ECR rows or fields;
- Cleaning transformations;
- Judgment inputs, scores, classifications, Action Ceiling, or Decision
  Strength;
- source-quality result tokens;
- credibility, relevance, inclusion, exclusion, sentiment, or quality decisions;
- commercial-use claims.

Visible listing labels may be recorded only as provenance fields when they are
needed to disambiguate the locator. They must not become body capture or ranking
evidence.

## Candidate Surfaces And Traversal

Candidate surfaces must be allowlisted and capped before the run.

Allowed source-specific surfaces may include search results, declared listings,
related containers, recommendations, cross-post-like relationships,
"more like this" surfaces, or outbound locator surfaces. A source-specific
artifact must name which surfaces are allowed and how they are capped.

Hard rule: a discovered candidate does not grant same-run traversal permission.

Entering a newly found container, following a recommended item, fetching an
outbound locator, expanding a relationship chain, or continuing past the
declared surface requires one of:

- a new run with a new `run_id`;
- an explicit scope amendment that preserves the prior stop reason and changed
  field;
- a separate promotion gate into an approved capture unit.

## Stop And Cap Model

Valid terminal run outcomes:

- `caps_reached`;
- `scope_exhausted`;
- `empty_result`;
- `blocked_result`;
- `operator_stop`;
- `hard_stop_triggered`;
- `commercial_reroute_required`.

Every run records one visible stop reason.

Empty-result, blocked-result, and capped-result are valid terminal outcomes.
They must not trigger automatic retry escalation into broader crawling.

Cap semantics:

- A cap is a bounded-work stop, not a sufficiency claim.
- `caps_reached` means only that the declared run stopped at its declared cap.
- It must not be reported as `done`, `complete`, `topic covered`, or "no more
  relevant candidates."
- The run must record `cap_type` and `coverage_claim`.

Allowed `cap_type` values:

- `probe`;
- `working_batch`;
- `high_recall_pass`.

Allowed `coverage_claim` values:

- `bounded_probe_only`;
- `bounded_batch_only`;
- `high_recall_attempt_with_limits`.

Numeric cap defaults are intentionally not set by this artifact. They are owner
policy decisions and may vary by source family, access risk, and run purpose.

## Promotion Gate

Candidate locators are inert planning context until promoted.

A promotion receipt must record:

- promoted locator;
- source family;
- originating `run_id`;
- candidate row identifier or stable row pointer;
- Decision Frame or approved capture-unit authority;
- capture purpose;
- selected downstream capture method or method family;
- non-promotion of all non-selected candidates;
- known limitations from the intake provenance receipt;
- confirmation that Source Capture Armory execution has not happened yet.

Promotion does not authorize broad crawling, body capture, packet generation, or
commercial acquisition beyond the selected capture unit. It only makes the
promoted locator eligible for a later authorized capture path.

## Subagent Boundary

Subagents may be used only as bounded intake workers inside one declared run.
They inherit the run envelope; they do not define or expand it.

Allowed subagent roles:

- scope-check worker;
- bounded enumeration worker;
- adversarial boundary worker;
- consolidation worker.

Subagents must not choose additional surfaces, widen scope, follow candidates,
fetch source bodies, capture packets, rank candidates, score source quality,
admit fixtures, or promote locators.

## Source-Family Specialization Requirements

Every source-family Candidate URL Intake artifact must define:

- source-family name;
- allowed candidate surfaces;
- required input envelope additions;
- source-container row specialization, if any;
- source-item row specialization, if any;
- outbound locator handling, if any;
- hard caps and stop reasons;
- same-run traversal stops;
- promotion gate into the downstream capture path;
- Armory bridge, if a later packet-producing path exists;
- explicit non-outputs.

Source-family artifacts may add fields only when they preserve the parent
contract. They must not remove the parent non-outputs, promotion gate, stop
model, cap semantics, secret prohibition, or no-same-run-traversal rule.

When a source-family artifact names an approved downstream access route, it must
also state whether that route is implemented for the candidate-intake use case,
implemented only for later capture, or still pending separate runtime support.

## Success Signals

A Candidate URL Intake lane is architecturally in-bounds only when all applicable
signals are checkable:

- bounded topic, source family, query, seed, or thematic scope exists before any
  run;
- allowed candidate surfaces are declared before execution;
- hard caps exist for each allowed candidate surface;
- time window or cutoff scope is declared when the source surface supports it;
- every run records a visible stop reason;
- empty-result, blocked-result, and capped-result are valid outcomes;
- no retry escalation into broad crawling;
- `caps_reached` carries `cap_type` and `coverage_claim`;
- continuation or widening is a new run or explicit scope amendment that
  preserves the prior stop reason;
- output is candidate locators plus provenance only;
- outbound locators are not fetched inside the current source-family intake;
- every candidate records method provenance, timestamp, source surface,
  query/listing path, sort/surface order, time/cutoff scope, caps, and exclusion
  receipt;
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

- source body capture;
- comment or discussion capture;
- profile or user capture;
- broad crawling;
- same-run traversal from candidate discovery surfaces;
- Source Capture Packet emission;
- parser/consolidation runner implementation;
- durable corpus or database creation;
- queue, scheduler, dashboard, deployment, or production runtime;
- commercial source acquisition;
- ECR, Cleaning, Judgment, fixture admission, or source-quality scoring.

Hard stops:

- source-family-wide walking;
- generic harvesting without a declared topic/theme/query/seed and caps;
- following discovered containers, accounts, profiles, replies, links,
  recommendations, cross-post-like relationships, related surfaces, outbound
  locators, or "more like this" surfaces inside the same run;
- treating `caps_reached`, `empty_result`, or `blocked_result` as completion,
  sufficiency, or topic coverage;
- no-entitlement gate bypass;
- stolen or nonconsensual credentials, cookies, or sessions;
- security exploits, malware, credential stuffing, or obvious cross-account,
  private, admin, confidential, or paywalled spillover once noticed;
- any method Orca would refuse to disclose internally;
- any secret-bearing row, receipt, sidecar, or artifact;
- monitored scope without both cadence and hard stop date;
- commercial, client-funded, buyer-facing, enterprise, scale, or data-licensing
  pressure before rerouting to sanctioned commercial/API paths.

## Artifact Placement

This parent contract belongs at:

`docs/product/data_capture_spine_candidate_url_intake_contract_v0.md`

Source-specific candidate-intake artifacts belong under `docs/product/` unless a
later owner decision creates a dedicated Candidate Signal Intake / Corpus Intake
artifact family.

This contract intentionally does not live under:

`docs/product/source_capture_toolbox/`

That folder is the Source Capture Armory product-doc home. Candidate URL Intake
is upstream of packet-producing Armory capture.

## Open Owner Questions

These questions do not block the parent architecture contract. They block
implementation defaults and promotion operations:

1. Should this contract later be superseded by a broader Candidate Signal Intake
   or Corpus Intake contract that includes non-URL candidate signals?
2. What numeric caps should apply by source family and `cap_type`?
3. Which candidate surfaces should be enabled by default, and which require
   explicit opt-in?
4. Should outbound locators be enabled by default or require explicit opt-in?
5. Should monitored/repeated candidate-intake runs be allowed before a Decision
   Frame?
6. Which lane owns the durable promotion receipt?

## Next Authorized Step

Allowed next step: source-specific docs-only alignment or owner decision on
defaults.

Implementation scoping is not allowed from this artifact alone. A future
implementation lane requires:

1. owner acceptance of this parent contract;
2. source-family specialization accepted for the target source;
3. explicit bounded build authorization;
4. validation gates that prove the implementation emits candidate rows and
   provenance only, without body capture, packet output, auto-promotion, or
   broad crawler behavior.

## Non-Claims

This artifact is not validation, readiness, source-access boundary amendment,
legal sufficiency, rights clearance, implementation authorization, live source
authorization, Source Capture Armory authorization, Source Capture Packet
generation, Data Capture handoff, ECR design, Cleaning design, Judgment design,
fixture admission, source-quality scoring, buyer proof, commercial acquisition
authorization, storage authorization, dashboard authorization, scheduler
authorization, deployment authorization, production-runtime authorization,
commit authorization, push authorization, or PR authorization.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "Orca now has a generic Capture Spine Candidate URL Intake parent contract for bounded candidate locator rows, run envelopes, provenance receipts, approved-downstream-access-route notation, cap/coverage semantics, no-same-run-traversal stops, outbound locator handling, transient source-family projection helpers that persist only candidate rows/provenance, subagent boundaries, and promotion gates before Source Capture Armory packet capture or Data Capture handoff; for Reddit, the downstream posture records CloakBrowser as the approved primary anti-blocking route and proxies as not blanket stop conditions without making intake invoke them."
  trigger: architecture_doctrine
  related_triggers:
    - output_authority
    - lifecycle_boundary
    - product_doctrine
  controlling_sources_updated:
    - "docs/product/data_capture_spine_candidate_url_intake_contract_v0.md"
    - "docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md"
    - "docs/workflows/data_capture_spine_consolidation_map_v0.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/decision-routing.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - ".agents/workflow-overlay/source-loading.md"
    - ".agents/workflow-overlay/retrieval-metadata.md"
    - ".agents/workflow-overlay/artifact-roles.md"
    - "docs/workflows/data_capture_spine_consolidation_map_v0.md"
    - "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
    - "docs/product/data_capture_source_access_boundary_decision_v0.md"
    - "docs/product/data_capture_source_access_method_plan_v0.md"
    - "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/README.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md"
    - "docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md"
  intentionally_not_updated:
    - path: "docs/workflows/orca_repo_map_v0.md"
      reason: "The top-level repo map already routes Data Capture detail through the Data Capture consolidation sub-map. The new parent contract is discoverable through that sub-map."
    - path: "forseti/product/spines/capture/core/source_capture_toolbox/README.md"
      reason: "Candidate URL Intake is explicitly upstream of Source Capture Armory. Adding the parent contract to the Armory README would blur ownership."
    - path: "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
      reason: "Commissioned-capture obligations did not change. The parent contract handles pre-Decision-Frame candidate locators and does not amend Data Capture obligations."
    - path: "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
      reason: "Build authorization did not change. This contract authorizes no runtime source access, crawler, packet runner, storage, dashboard, scheduler, deployment, or production runtime."
  stale_language_search: "rg -n \"Candidate URL Intake|candidate locator|candidate_or_scouting|promotion gate|cap_type|coverage_claim|same-run traversal|outbound locator|approved_downstream_access_route|transient projection|parser output|raw HTML|CloakBrowser|proxy|proxies|Source Capture Packet output|auto-promotion\" docs/product/data_capture_spine_candidate_url_intake_contract_v0.md docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md docs/workflows/data_capture_spine_consolidation_map_v0.md forseti/product/spines/capture/core/source_capture_toolbox/README.md forseti/product/spines/capture/core/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not owner acceptance"
    - "not source-access boundary amendment"
    - "not implementation authorization"
    - "not live source authorization"
    - "not broad crawling authorization"
    - "not Source Capture Packet generation"
    - "not Data Capture handoff"
    - "not ECR, Cleaning, Judgment, fixture admission, source-quality scoring, or commercial authorization"
```
