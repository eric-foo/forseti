# Data Capture Spine LinkedIn Lane Discovery Planning Architecture v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture contract
scope: Defines the LinkedIn Lane as a bounded discovery and candidate-frontier lane for businesses, organizations, senior decision makers, public professional actors, creators, and influential people before any source capture, outreach, or commercial use.
use_when:
  - Planning LinkedIn-adjacent discovery without turning it into LinkedIn scraping.
  - Checking the optional supervised POC-risk browser-assist mode and its guardrails.
  - Distinguishing decision-evidence discovery from future lead/outreach handling.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_candidate_url_intake_contract_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/linkedin_reddit_source_capture_armory_concurrent_structure_architecture_v0.md
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
  - orca/product/spines/capture/core/contracts/source_access_boundary/data_capture_source_access_boundary_decision_v0.md
stale_if:
  - LinkedIn platform policy, API, Sales Navigator, or source-access posture changes.
  - The Candidate URL Intake parent contract changes candidate rows, run envelopes, promotion gates, caps, or traversal stops.
  - Orca creates a separate Outreach Lane, contact acquisition policy, or commercial LinkedIn authorization.
  - The owner changes the personal/pre-commercial POC risk posture.
```

## Status

Status: `OWNER_ACCEPTED_LINKEDIN_LANE_DISCOVERY_PLANNING_V0`.

Owner decision recorded 2026-06-08:

- Use the memorable name **LinkedIn Lane**.
- Treat supervised agent/browser-assist work as green inside the lane when it is
  tagged as `optional_poc_risk_mode` and obeys the guardrails below.
- Do not track every post by a person forever.
- Bounded public-actor watch is acceptable for defined periods, especially for
  commissioned or Decision-Frame-bound work.
- Visible influence numbers may be recorded when they help assess public
  professional influence.
- Senior-role / decision-maker discovery may be in scope; junior-role org-chart
  mining is out of scope.
- Lead harvesting and contact acquisition belong in a separate future Outreach
  Lane. This LinkedIn Lane can lay the foundation by producing promoted
  candidates, but it must not harvest contacts.
- Supervised browser-assist may use anti-blocking techniques (anti-detect /
  cloaked browser, residential / rotating proxies, in-browser JS-challenge
  handling) to reach discoverable or entitled surfaces under
  `optional_poc_risk_mode`, consistent with the source-access boundary;
  bypassing an entitlement gate to reach non-entitled data remains a hard stop.

This artifact is not implementation authorization. It does not authorize a live
LinkedIn runner, autonomous scraping, bulk export, contact harvesting, lead-list
creation, profile dataset construction, storage, scheduler, dashboard,
production runtime, commercial use, ECR, Cleaning, Judgment, buyer proof,
commits, pushes, or PRs.

## Meaning Of Optional POC Risk Mode

`optional_poc_risk_mode` means:

```text
Allowed for Orca's personal / pre-commercial proof-of-concept work, with owner-
accepted ToS, account, reputation, and platform-enforcement risk, when the run is
operator-supervised, bounded, provenance-recorded, non-commercial, and stopped
on friction or person-data drift. Under this mode the supervised session may use
anti-blocking techniques (anti-detect / cloaked browser configuration, residential
or rotating proxy integration, and in-browser JS-challenge handling) to reach
discoverable or entitled LinkedIn surfaces, consistent with Orca's source-access
boundary (discoverable-or-entitled + disclosable). "Supervised" means the operator
runs and watches the session and it is provenance-recorded; it does not require a
non-cloaked browser.
```

It does **not** mean:

- LinkedIn permits or sanctions the method;
- the method is legally sufficient;
- the method is commercial-ready;
- agents may run unattended;
- broad scraping is allowed;
- profile/contact/network harvesting is allowed;
- output may become a person dossier, lead list, or captured source packet (CapturePacket);
- bypassing an entitlement gate to reach data the operator is not entitled to is
  allowed (no-entitlement gate bypass remains a hard stop);
- anti-blocking on discoverable/entitled surfaces extends to non-entitled,
  private, or gated material.

In short: it is green for Orca POC routing, not green as a platform/legal claim.

## Lane Position

The LinkedIn Lane is upstream of Source Capture Armory and upstream of any future
Outreach Lane.

```text
LinkedIn Lane
  1. Discovery
  2. Bounded Watch
  3. Graph Frontier Register
  4. Semantic Projection
  5. Promotion Decision
  6. Later Capture or Outreach Lane, if separately authorized
```

Source Capture Armory may consume a promoted locator later, but this lane does
not invoke packet runners, preserve source bodies, or hand material to Data
Capture by default.

Outreach may later consume a promoted business or public-professional candidate,
but this lane does not collect emails, phone numbers, private contact routes,
lead lists, connection graphs, or commenter leads.

## Run Envelope

A LinkedIn Lane run is invalid unless these fields are declared before the run:

- `run_id`;
- `declared_theme_or_decision_context`;
- `run_purpose`;
- `candidate_classes`;
- `source_surface_allowlist`;
- `method_mode`;
- `optional_poc_risk_mode`: `yes` or `no`;
- `non_commercial_posture`;
- caps for businesses, organizations, people, source surfaces, and time;
- `watch_window_or_none`;
- `stop_condition`;
- exclusions;
- source-policy posture;
- minimization rule;
- promotion owner.

Allowed `method_mode` values:

- `manual_operator_browsing`;
- `sales_navigator_manual_entitled`;
- `operator_supplied_link_or_note`;
- `agent_assisted_rowing_only`;
- `supervised_browser_assist_optional_poc_risk`.

`agent_assisted_rowing_only` means the agent can structure, classify, dedupe,
and register operator-supplied observations. It does not browse LinkedIn.

`supervised_browser_assist_optional_poc_risk` means the agent may assist an
operator-supervised, provenance-recorded browser session under this artifact's
guardrails, including anti-blocking techniques (anti-detect / cloaked browser,
residential or rotating proxies, in-browser JS-challenge handling) to reach
discoverable or entitled LinkedIn surfaces. It must not be used as a background
scraper or generalized automation route, and it must not bypass an entitlement
gate to reach data the operator is not entitled to.

## Candidate Classes

Allowed candidate classes:

- `business`;
- `organization`;
- `public_professional_actor`;
- `senior_decision_maker`;
- `executive`;
- `creator_or_influencer`;
- `analyst_or_investor`;
- `event_or_public_role_actor`.

People candidates must carry stricter flags than business candidates.

Ordinary people, junior employees, non-public staff, commenters, followers, and
connections are not default candidate classes. A junior person may be included
only when they are independently a public professional actor for the declared
theme, not because they appear in an org chart.

A person qualifies as `public_professional_actor` or `senior_decision_maker`
only when at least one independent public-actor basis is recorded in
`senior_role_or_public_actor_basis_or_none` with a concrete pointer, drawn from:

- a named public speaking, publication, press, interview, podcast, or newsletter
  appearance under their own name;
- an official public spokesperson, founder, executive, or named decision-maker
  role for the declared theme;
- a self-published public professional or creator presence they own, not a
  routine employer-feed post.

The basis must stand outside the employer org chart. Appearing in an org chart,
being mentioned or tagged by others, posting routine work updates, or being a
commenter, follower, or connection is not a qualifying basis. If no such basis
can be recorded, the person is held or quarantined, not promoted.

Visible influence numbers (counts or coarse bands) and their trajectory over
time may *corroborate* a qualifying basis and prioritize watch, but are never
themselves a qualifying basis; a small-but-fast-rising ("meteoric") actor may be
flagged for watch on the trajectory of visible numbers, not on the social graph.
Trajectory tracking is a deferred Bounded Watch capability — see
`docs/product/data_capture_spine_linkedin_influence_trajectory_watch_spec_v0.md`.

## Candidate Row Schema

```yaml
candidate_id:
run_id:
capture_unit_intake_status: candidate_or_scouting
source_family: linkedin_adjacent
candidate_class:
entity_type: business_entity | organization_entity | individual_person
display_name:
canonical_locator_or_none:
source_locators:
source_surface:
source_policy_posture:
method_mode:
optional_poc_risk_mode: yes | no
declared_theme_or_decision_context:
run_purpose:
business_relevance_note:
role_or_influence_basis_or_none:
senior_role_or_public_actor_basis_or_none:
visible_influence_numbers:
  follower_count_or_none:
  connection_count_band_or_none:
  subscriber_count_or_none:
  engagement_count_or_none:
influence_number_source_surface_or_none:
privacy_sensitivity: business_low | person_strict | public_actor_strict | quarantine
minimization_rule: business_entity_only | name_role_locator_only | no_contact_fields | review_required
person_data_minimized: yes | no | not_applicable
contact_fields_retained: no
network_or_follower_list_retained: no
profile_body_captured: no
content_captured: no
excluded_fields_receipt:
provenance_timestamp:
visible_stop_reason_if_any:
allowed_downstream_use: planning_only
promotion_required: yes
```

Allowed influence numbers are visible counts or coarse visible bands only. They
are influence context, not network capture. The lane must not persist follower
lists, connection lists, commenter lists, or relationship graphs.

## Graph Frontier Register Additions

The Graph Frontier Register may persist planning structure only.

Allowed node types:

- `business_candidate`;
- `organization_candidate`;
- `public_professional_actor_candidate`;
- `senior_decision_maker_candidate`;
- `creator_or_influencer_candidate`;
- `source_locator`;
- `theme`;
- `run`;
- `frontier_decision`;
- `stop_event`.

Allowed edge types:

- `discovered_from_run`;
- `found_on_source_surface`;
- `same_theme_overlap`;
- `same_company_or_org_context`;
- `public_role_context`;
- `source_locator_overlap`;
- `prior_seen`;
- `selected_as_frontier`;
- `held_for_review`;
- `quarantined_privacy`;
- `dead_end`.

Forbidden graph outputs:

- follower graph;
- connection graph;
- commenter graph;
- employment-history graph;
- full org chart;
- contact graph;
- lead list.

`public_role_context` is allowed only to explain why the actor matters to the
declared business theme or decision. It must not become general person tracking.

## Semantic Projection

Semantic Projection may classify candidates as:

- `promote`;
- `hold`;
- `quarantine`;
- `dead_end`.

Projection may consider business fit, role materiality, public influence,
source-surface posture, duplication, privacy risk, and whether the candidate is
inside the declared theme.

Projection must not:

- promote automatically;
- capture content;
- collect contacts;
- score source quality;
- decide Decision Strength or Action Ceiling;
- claim coverage or sufficiency;
- hand material to Data Capture, ECR, Cleaning, or Judgment.

## Allowed Source-Surface Matrix

| Source surface | Business / org candidates | People candidates | Posture |
| --- | --- | --- | --- |
| Operator-supplied seed list | allowed | allowed with minimization | Best initial mode. |
| Company website, blog, docs, pricing, changelog, press page | allowed | allowed only when role is material | Official or semi-official business surface. |
| Conference, podcast, newsletter, webinar, public interview, publication | allowed | allowed | Good public-professional actor surface. |
| Public directory or ecosystem list | allowed | allowed with minimization | Record policy/source posture. |
| Manual search result review | allowed | allowed with minimization | Candidate locator only. |
| Sales Navigator manual entitled UI | allowed | allowed with strict minimization | First-party entitled surface; no bulk export. |
| LinkedIn company page or post manually reviewed | allowed | allowed only as role/context signal | Candidate or business-signal note only. |
| LinkedIn public/person URL manually reviewed | non-default | allowed only for public professional actor or senior decision-maker context | No profile body capture. |
| Supervised browser-assist optional POC risk mode (anti-blocking on discoverable/entitled surfaces) | allowed | allowed with strict minimization | Green for Orca POC only; risk-tag required; anti-detect/proxy/JS-challenge permitted to reach discoverable/entitled surfaces; no-entitlement gate bypass excluded. |
| Automated LinkedIn scraping, unattended agent browsing, bulk export | blocked | blocked | Hard stop. |
| Contact enrichment, follower list, connection graph, commenter harvesting | blocked in this lane | blocked in this lane | Future Outreach Lane or separate decision only. |

## Bounded Watch

Bounded watch is allowed when all are true:

- actor or business list is declared before the run;
- theme or Decision Frame is declared;
- watch window and stop date are declared;
- caps are declared;
- only relevant public/professional posts or observations are noted;
- no full timeline is built;
- no contact fields are retained;
- no follower or connection lists are retained;
- every row remains planning-only unless promoted.

This permits watching key public professional actors for a commissioned period.
It does not permit indefinite tracking of a person's whole public life.

## Promotion Gate

Promotion requires a separate receipt recording:

- promoted candidate id;
- originating run id;
- candidate class and entity type;
- exact locator;
- reason for promotion;
- known limitations;
- privacy/minimization flags;
- selected downstream lane: `source_capture`, `data_capture`, or
  `future_outreach`;
- lawful source-access or outreach method to be decided later;
- non-promotion of non-selected candidates;
- confirmation that no capture, contact harvesting, or outreach has happened.

Promotion does not itself authorize capture, contact acquisition, outreach,
Source Capture Packet generation, Data Capture handoff, commercial use, or
automated LinkedIn access.

## Hard Stops

These are run-time behaviors that must not occur in any LinkedIn Lane run (the
operational stop list; authority this artifact does not confer is in Non-Claims
below):

- unattended LinkedIn automation;
- autonomous scraping;
- background runs;
- bulk export;
- no-entitlement gate bypass;
- stolen or nonconsensual credentials, cookies, sessions, storage state, or
  browser profiles;
- private messages, private groups, admin/confidential/cross-account spillover;
- profile body harvesting;
- contact harvesting;
- emails, phone numbers, private contact routes, or enrichment output;
- follower, connection, commenter, or relationship-list retention;
- junior-role org chart mining;
- full org chart construction;
- lead-list creation;
- source body/content capture;
- Source Capture Packet output;
- Data Capture handoff;
- ECR, Cleaning, Judgment, source-quality scoring, fixture admission, buyer
  proof, commercial use, storage, scheduler, dashboard, deployment, or
  production runtime.

## Attended-Automation POC-Risk Variant

The "unattended LinkedIn automation / background runs" hard stop forbids
operation with **no owner present**. An **owner-present attended-automation** run
is a separately opted-in POC-risk exception (`method_mode:
owner_present_attended_automation_optional_poc_risk`, `optional_poc_risk_mode:
yes`) — it is not a "background run" because the owner is present — allowed only
when all bind:

- the owner is present at the machine, enforced by a **programmatic presence
  check** that halts the run if presence lapses;
- the same source-access boundary (`discoverable-or-entitled + disclosable`), run
  envelope, caps, minimization rule, acceptance gate, and hard stops verbatim as
  every other run;
- **`no-entitlement gate bypass` to non-entitled data remains a hard stop**;
- a stop-on-friction / stop-on-person-data-drift rule.

Caveat (recorded, not waved): a presence check proves the owner is *present*, not
that they *supervise each action*, and it does **not** make automated access
ToS-compliant. It is green for Orca personal / pre-commercial POC routing only —
not a platform, legal, or commercial claim. Truly-unattended (no owner present)
operation stays a hard stop.

## Smallest Implementation Scope

No implementation is authorized by this artifact alone.

If implementation is later authorized, the smallest safe scope is local and
no-live:

1. a row schema/template;
2. a Graph Frontier Register template/helper over operator-supplied rows;
3. validation that forbidden fields do not exist;
4. validation that every person row carries privacy/minimization flags;
5. validation that every run has caps, stop condition, and non-claims;
6. validation that no source body, profile body, contact, follower list,
   connection list, Source Capture Packet, or promotion output is emitted.

Live browser-assist implementation would need a separate bounded execution
authorization and validation gates.

## Non-Claims

These name authority this artifact does not confer (the authority-boundary list;
operational run-time stops are in Hard Stops above). This artifact is not:

- LinkedIn platform permission;
- legal advice;
- legal sufficiency;
- commercial authorization;
- live LinkedIn authorization;
- autonomous scraping authorization;
- broad automation authorization;
- no-entitlement gate bypass authorization;
- contact acquisition authorization;
- outreach authorization;
- lead-list authorization;
- follower/connection graph authorization;
- Source Capture Armory execution;
- Source Capture Packet output;
- Data Capture handoff;
- ECR, Cleaning, Judgment, fixture admission, source-quality scoring, buyer
  proof, validation, readiness, storage, scheduler, dashboard, deployment, or
  production-runtime authorization.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "Orca now has an owner-accepted LinkedIn Lane discovery-planning architecture that treats supervised browser-assist as green for personal/pre-commercial POC only when tagged optional_poc_risk_mode, bounded, operator-supervised, provenance-recorded, non-commercial, and minimized; under that mode it may use anti-blocking techniques (anti-detect/cloaked browser, residential/rotating proxies, in-browser JS-challenge handling) to reach discoverable or entitled surfaces consistent with the unchanged source-access boundary, while no-entitlement gate bypass to non-entitled data, contact acquisition, and lead harvesting remain hard stops or belong to a separate future Outreach Lane."
  trigger: architecture_doctrine
  related_triggers:
    - product_doctrine
    - lifecycle_boundary
    - output_authority
  controlling_sources_updated:
    - "docs/product/data_capture_spine_linkedin_discovery_planning_lane_architecture_v0.md"
    - "orca/product/spines/capture/core/source_capture_toolbox/linkedin_reddit_source_capture_armory_concurrent_structure_architecture_v0.md"
    - "docs/workflows/data_capture_spine_consolidation_map_v0.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - ".agents/workflow-overlay/artifact-folders.md"
    - ".agents/workflow-overlay/retrieval-metadata.md"
    - "docs/product/data_capture_spine_candidate_url_intake_contract_v0.md"
    - "docs/product/data_capture_source_access_boundary_decision_v0.md"
    - "docs/product/data_capture_source_access_method_plan_v0.md"
    - "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
    - ".agents/workflow-overlay/safety-rules.md"
    - "orca/product/spines/capture/core/source_capture_toolbox/linkedin_reddit_source_capture_armory_concurrent_structure_architecture_v0.md"
    - "docs/workflows/data_capture_spine_consolidation_map_v0.md"
  intentionally_not_updated:
    - path: "orca/product/spines/capture/core/source_capture_toolbox/README.md"
      reason: "LinkedIn Lane discovery is upstream of Source Capture Armory and does not emit Source Capture Packets."
    - path: "docs/product/data_capture_spine_candidate_url_intake_contract_v0.md"
      reason: "The parent Candidate URL Intake contract already owns generic row/provenance and promotion-gate rules; this source-family artifact specializes entity/person handling."
    - path: "docs/product/data_capture_source_access_boundary_decision_v0.md"
      reason: "The controlling boundary already permits disclosable anti-blocking to reach discoverable/entitled material and already hard-stops no-entitlement gate bypass; this lane edit stays inside that boundary and changes no controlling permission or hard stop."
    - path: "docs/product/data_capture_source_access_method_plan_v0.md"
      reason: "The method plan already classifies anti-detect/proxy as in-bounds for discoverable/entitled material under owner-accepted risk; the LinkedIn lane consumes that posture without changing it."
    - path: "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
      reason: "The third-tranche anti-detect/proxy/JS-challenge build authorization is unchanged; this is a docs-only lane posture edit, not a build or runtime authorization."
    - path: ".agents/workflow-overlay/safety-rules.md"
      reason: "Safety-rules preserves the third-tranche anti-detect/proxy scope and bounded-implementation gating; no hard stop or gate is weakened by this lane posture edit."
  stale_language_search: "rg -n \"optional_poc_risk_mode|anti-detect|cloaked browser|residential|rotating prox|JS-challenge|no-entitlement gate bypass|discoverable or entitled|honest|visible operator-supervised|lead list|contact harvesting|follower graph|connection graph\" docs/product/data_capture_spine_linkedin_discovery_planning_lane_architecture_v0.md orca/product/spines/capture/core/source_capture_toolbox/linkedin_reddit_source_capture_armory_concurrent_structure_architecture_v0.md docs/workflows/data_capture_spine_consolidation_map_v0.md docs/product/data_capture_source_access_boundary_decision_v0.md .agents/workflow-overlay/safety-rules.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not legal sufficiency"
    - "not live LinkedIn authorization"
    - "not Source Capture Packet generation"
    - "not Outreach Lane authorization"
    - "not commercial authorization"
```

```yaml
# Appended 2026-06-10 (owner-accepted D1 + D5).
direction_change_propagation:
  doctrine_changed: "Two owner-accepted refinements. (D1) Visible influence numbers and their trajectory over time may corroborate a public-actor basis and prioritize watch but are never themselves a qualifying basis; meteoric-rise detection rides on the trajectory of visible counts, NOT the social graph, and is a deferred Bounded Watch capability specced separately. (D5) An owner-present attended-automation POC-risk variant (method_mode owner_present_attended_automation_optional_poc_risk) is a separately opted-in exception to the unattended/background-run hard stop, gated by a programmatic owner-presence check that halts on presence lapse, binding the same boundary/caps/minimization/acceptance-gate/hard-stops verbatim with no-entitlement gate bypass still hard-stopped; a presence check proves presence not per-action supervision and does not cure ToS, and truly-unattended operation stays a hard stop."
  trigger: architecture_doctrine
  related_triggers:
    - product_doctrine
    - lifecycle_boundary
  controlling_sources_updated:
    - "docs/product/data_capture_spine_linkedin_discovery_planning_lane_architecture_v0.md"
    - "docs/workflows/linkedin_lane_operator_pilot_plan_v0.md"
    - "orca-harness/capture_spine/linkedin_lane/models.py"
    - "docs/product/data_capture_spine_linkedin_influence_trajectory_watch_spec_v0.md"
  downstream_surfaces_checked:
    - "orca-harness/capture_spine/linkedin_lane/validation.py"
    - "docs/product/data_capture_spine_future_exploration_lanes_v0.md"
  intentionally_not_updated:
    - path: "orca-harness/capture_spine/linkedin_lane/validation.py"
      reason: "D1 adds no validator rule (a concrete basis is still required; influence is already captured). D5 adds a MethodMode member only; the presence check is a live-runner concern, and the closed-enum validator already accepts any MethodMode value, so the no-live slice needs no validator change."
    - path: "source-access boundary / safety-rules / build-authorization decisions"
      reason: "D5 stays inside the existing discoverable-or-entitled boundary and the no-entitlement-gate-bypass hard stop; no controlling permission, boundary, or safety rule is weakened."
  non_claims:
    - "not validation"
    - "not readiness"
    - "not live LinkedIn authorization"
    - "not a presence-check implementation"
    - "not the social graph"
    - "not Bounded Watch implementation authorization"
```
