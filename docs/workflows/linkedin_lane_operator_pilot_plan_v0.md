# LinkedIn Lane Operator Pilot Plan v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow plan
scope: >
  Defines the operator-pilot / bounded-run layer above the accepted LinkedIn
  Lane discovery-planning architecture: a single bounded discovery run, walked
  stage by stage with guardrails inline, that produces planning-only candidate
  rows + Graph Frontier planning structure + an operator promotion decision,
  with no source capture, contact acquisition, or outreach.
use_when:
  - Running (or scoping) one bounded LinkedIn Lane discovery pilot after the architecture is accepted.
  - Deciding what the operator and the agent each do across the lane's six stages without widening into capture or outreach.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_discovery_planning_lane_architecture_v0.md
  - orca/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_candidate_url_intake_contract_v0.md
  - orca/product/spines/capture/core/contracts/source_access_boundary/data_capture_source_access_boundary_decision_v0.md
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
stale_if:
  - The LinkedIn Lane architecture changes stages, run envelope, candidate classes, row schema, source-surface matrix, bounded-watch posture, promotion gate, or hard stops.
  - The Candidate URL Intake parent contract changes run envelopes, rows, caps, traversal stops, or promotion gates.
  - The owner changes the personal/pre-commercial POC-risk posture or the source-access boundary.
```

## Status

Status: `OPERATOR_PILOT_LAYER_RECOMMENDED`.

This plan operationalizes the **accepted** LinkedIn Lane discovery-planning
architecture (`docs/product/data_capture_spine_linkedin_discovery_planning_lane_architecture_v0.md`).
It adds sequencing and a default no-live pilot mode; it confers **no new
permission**. It does not authorize a live LinkedIn runner, autonomous scraping,
supervised browser-assist by default, no-entitlement gate bypass, contact
acquisition, lead lists, follower/connection/commenter graph capture, profile
body or content capture, Source Capture Packets, Data Capture handoff, ECR,
Cleaning, Judgment, storage, scheduler, dashboard, production runtime,
commercial use, Outreach Lane execution, commits, pushes, or PRs.

## Layer Definition

The layer above the accepted architecture is the **operator-pilot / bounded-run
layer**. The architecture proves the lane can hold its boundaries on paper; the
pilot proves the lane can be used for one real operator decision:

```text
Given a declared theme / decision context and a bounded, discoverable-or-entitled
LinkedIn-adjacent source surface, can the lane produce planning-only candidate
rows (+ Graph Frontier planning structure) with privacy/minimization intact, a
visible stop reason, and no forbidden capture/contact/graph behavior?
```

The layer ends at candidate rows, Graph Frontier register entries, run
provenance, and an operator decision about whether any candidate should later
enter the separate promotion gate. It is **not** Source Capture Armory and
**not** a future Outreach Lane.

## Cynefin Routing

- **Smallest complete outcome:** define one bounded pilot envelope + acceptance
  gate so the next execution can test operator usefulness without widening scope.
- **Regime:** complicated, with a **people-data + POC-risk edge**.
- **Why:** the accepted architecture and the source-access boundary exist, but
  person-data minimization and the supervised-browser-assist risk posture must
  not enter by implication.
- **Decomposition:** layer-based. Keep discovery, bounded watch, graph frontier,
  semantic projection, and promotion separate from later capture / outreach.
- **Current bottleneck:** choosing one pilot envelope + success gate before any
  run creates candidate rows (especially person rows) that could be overclaimed
  or under-minimized.
- **Riskiest assumption:** a bounded discovery run is useful without treating
  `caps_reached` as coverage, without same-run frontier traversal, and without
  promoting candidates automatically.
- **Stop or pivot condition:** if the pilot needs profile-body capture, contact
  fields, follower/connection/commenter retention, content capture, Source
  Capture Packet output, Data Capture handoff, or outreach to count as success,
  it is trying to leave the lane and must be rerouted.
- **Allowed next move:** run or scope one bounded pilot under this plan.
- **Disallowed next move:** scraping, unattended browsing, bulk export, contact
  harvesting, lead lists, graph capture, capture-packet generation, or promotion
  by implication.

## Pilot Envelope

**Default pilot mode:** `pilot_no_live_operator_supplied_observations`
(`optional_poc_risk_mode: no`).

In this default mode the operator browses **discoverable or entitled**
LinkedIn-adjacent surfaces **manually and outside the lane** (or uses an
operator-supplied seed list / saved note), and supplies observations to the
agent. The agent runs in **`agent_assisted_rowing_only`** mode: it structures,
classifies, dedupes, and registers operator-supplied observations into candidate
rows. **The agent does not browse LinkedIn in the default pilot.** Supervised
browser-assist is the separately-escalated variant below.

Required pilot envelope (the architecture's Run Envelope, filled with pilot
defaults + operator placeholders):

```yaml
run_id: linkedin_lane_pilot_001
declared_theme_or_decision_context: <operator declares before run>   # e.g. a decision context for competitor X; do not assume a frozen wedge
run_purpose: bounded operator pilot for LinkedIn Lane discovery
candidate_classes: [business, organization, public_professional_actor, senior_decision_maker]  # operator narrows
source_surface_allowlist:                                            # discoverable-or-entitled only
  - operator_supplied_seed_list
  - company_website_blog_press_pricing
  - conference_podcast_newsletter_publication
  - public_directory_or_ecosystem_list
  - manual_search_result_review
  - sales_navigator_manual_entitled        # only if operator is entitled; strict minimization
method_mode: agent_assisted_rowing_only    # default; manual_operator_browsing / operator_supplied_link_or_note also allowed
optional_poc_risk_mode: no                 # default OFF; the supervised-browser-assist variant must opt in
non_commercial_posture: pre_commercial
caps:
  max_businesses: 25
  max_organizations: 25
  max_people: 15
  max_source_surfaces: 5
  time_window_days: 30
watch_window_or_none: none                 # bounded watch is opt-in with its own window + stop date
stop_condition: caps_reached | scope_exhausted | empty_result | blocked_result | privacy_drift | operator_stop
exclusions: []                             # declared even when empty
source_policy_posture: discoverable_or_entitled_disclosable
minimization_rule: business_entity_only | name_role_locator_only | no_contact_fields | review_required
promotion_owner: <operator>
```

The pilot may choose lower caps. It must not exceed these `probe` defaults
without a new scope amendment or owner decision.

## Inputs

Required before pilot execution:

- declared theme / decision context;
- narrowed candidate classes;
- the discoverable-or-entitled source surfaces in scope;
- operator-supplied seed list, saved notes, or observations (default no-live mode);
- caps (defaults above, or lower);
- declared exclusions, even when empty;
- declared stop-condition expectation;
- whether a bounded watch window is in scope (default: none);
- non-commercial posture.

Optional but useful:

- why this theme matters to the next planning decision;
- what would make the operator promote one candidate later;
- known limitations of the supplied observations (stale, partial, single-surface).

## The Run, Stage By Stage (the operating procedure)

Walk only the stages the envelope declares. Each stage names the **operator**
action, the **agent (rowing-only)** action, the **inline guardrails**, and the
**stop checks**.

1. **Discovery.**
   - Operator: browses the declared discoverable/entitled surfaces (or supplies
     the seed list / notes) and hands observations to the agent.
   - Agent: rows each observation into a candidate row (architecture Candidate
     Row Schema), sets `entity_type`, `candidate_class`, locators, and
     `business_relevance_note`; dedupes against this run.
   - Guardrails: business/org rows are low-sensitivity; **every person row must
     carry a `senior_role_or_public_actor_basis_or_none` with a concrete pointer
     drawn from the architecture's allowed bases** — a named public appearance
     under the person's own name (speaking / publication / press / interview /
     podcast / newsletter), an official spokesperson / founder / executive /
     named-decision-maker role for the declared theme, or an owned public
     professional / creator presence. **Org-chart presence, mentions or tags by
     others, routine employer-feed posts, and commenter / follower / connection
     status are NOT a qualifying basis.** No qualifying pointer ⇒
     `hold`/`quarantine`, never promoted. No contact fields, no profile
     body, no content.
   - Stop checks: caps reached; empty result; blocked result; `privacy_drift`
     (a person can't be qualified without an org-chart-independent basis).

2. **Bounded Watch** *(only if `watch_window_or_none` is set).*
   - Operator: declares the actor/business list, the watch window, the stop date,
     and the caps **before** watching; notes only relevant public/professional
     observations.
   - Agent: rows watch observations against existing candidate rows; records
     visible influence numbers (counts / coarse bands) when they help assess
     public influence.
   - Guardrails: no full timeline; no contact fields; **no follower/connection/
     commenter list retention**; every row stays planning-only. Watching a
     person's whole public life is out of scope.
   - Stop checks: window elapsed; stop date reached; caps reached; privacy drift.

3. **Graph Frontier Register.**
   - Operator/agent: persist **planning structure only** — allowed node types
     (business/organization/public-professional/senior-decision-maker/creator
     candidates, source_locator, theme, run, frontier_decision, stop_event) and
     allowed edge types (discovered_from_run, found_on_source_surface,
     same_theme_overlap, public_role_context, …).
   - Guardrails: **forbidden graph outputs** — follower graph, connection graph,
     commenter graph, employment-history graph, full org chart, contact graph,
     lead list. `public_role_context` explains why an actor matters to the theme;
     it must not become general person tracking.
   - Stop checks: a frontier hop needs a **new run** (new `run_id`, caps,
     exclusions, stop condition) — **no same-run traversal**.

4. **Semantic Projection.**
   - Agent: classify each candidate `promote` / `hold` / `quarantine` /
     `dead_end`, considering business fit, role materiality, public influence,
     source-surface posture, duplication, privacy risk, and theme membership.
   - Guardrails: projection must **not** auto-promote, capture content, collect
     contacts, score source quality, decide Decision Strength / Action Ceiling,
     claim coverage/sufficiency, or hand material to Data Capture/ECR/Cleaning/
     Judgment. (Note: "business fit" is operator-declared per the theme — do not
     bake an unratified pricing/wedge rubric into projection.)
   - Stop checks: any candidate needing capture/contact/graph to be judged "fit"
     is out of scope.

5. **Promotion Decision.**
   - Operator: for any `promote` candidate, a **separate promotion receipt** must
     be opened (promoted id, originating run, class/entity, exact locator, reason,
     known limitations, privacy/minimization flags, selected downstream lane,
     confirmation no capture/contact/outreach happened).
   - Guardrails: promotion **does not** itself authorize capture, contact
     acquisition, outreach, Source Capture Packet generation, Data Capture
     handoff, commercial use, or automated LinkedIn access.
   - Stop checks: non-selected candidates are explicitly **not** promoted.

## Outputs

Allowed pilot outputs:

- candidate rows (architecture Candidate Row Schema), planning-only;
- Graph Frontier Register entries (allowed node/edge types only);
- run-level provenance receipt;
- a bounded, operator-held local planning artifact (JSON/Markdown) holding this run's rows / register / closeout — **not** a database, reusable people dataset, durable datastore, scheduler, dashboard, or product/runtime storage;
- a pilot closeout note (row counts, stop reason, forbidden-output checks, non-claims).

Explicit non-outputs:

- profile bodies; post/content text; raw page captures or screenshots as data;
- contact fields (emails, phone numbers, private contact routes), enrichment;
- follower / connection / commenter / relationship lists or graphs;
- employment-history graphs, full org charts, lead lists;
- ordinary-person / junior-staff rows lacking a public-actor basis;
- Source Capture Packets; Data Capture handoff;
- promotion receipts unless separately opened;
- ECR, Cleaning, Judgment, fixture admission, source-quality scoring, buyer
  proof, or commercial-use claims.

## Acceptance Gate

The pilot is acceptable only if **all** are true (each condition is observable in
the output artifacts):

- the run envelope is fully declared before execution;
- output contains candidate rows + Graph Frontier planning structure + provenance only;
- every candidate row is `capture_unit_intake_status: candidate_or_scouting` and `allowed_downstream_use: planning_only`, with `promotion_required: yes`;
- **every person row** carries a `senior_role_or_public_actor_basis_or_none` with a concrete qualifying pointer from the architecture's allowed source categories (and none drawn from an excluded basis — org chart, mention/tag, routine post, commenter/follower/connection), plus a `privacy_sensitivity` flag, a `minimization_rule`, and `person_data_minimized` set;
- `contact_fields_retained: no`, `network_or_follower_list_retained: no`, `profile_body_captured: no`, `content_captured: no` on every row;
- visible influence numbers, if present, are counts or coarse bands only — no follower/connection/commenter lists;
- caps, a visible stop reason, and non-claims are recorded; `caps_reached` is **not** described as coverage or sufficiency;
- no same-run frontier traversal occurred (each hop = a new run);
- no forbidden graph output exists (follower/connection/commenter/employment/org-chart/contact graph, lead list);
- empty-result, blocked-result, and `privacy_drift` (a person can't be qualified) remain **valid** outcomes if encountered;
- output non-claims include: no live LinkedIn access, no supervised browser-assist (unless the variant was explicitly opted into), no Source Capture Packet, no auto-promotion, no Data Capture handoff, no outreach.

## Optional POC-Risk Variant (supervised browser-assist) — separately escalated

This plan's default does **not** invoke it. A pilot may opt into
`method_mode: supervised_browser_assist_optional_poc_risk` with
`optional_poc_risk_mode: yes` only when it additionally binds:

- the source-access boundary (`discoverable-or-entitled + disclosable`);
- operator-supervised, provenance-recorded session (operator runs and watches it);
- anti-blocking (anti-detect / cloaked browser, residential/rotating proxies,
  in-browser JS-challenge handling) used **only** to reach discoverable or
  entitled surfaces;
- the same run envelope, caps, minimization rule, and acceptance gate above;
- the hard stops verbatim, with **`no-entitlement gate bypass` to non-entitled
  data remaining a hard stop** (anti-blocking on discoverable/entitled surfaces
  never extends to private/gated material);
- a stop-on-friction / stop-on-person-data-drift rule.

It remains green for Orca personal / pre-commercial POC routing only — not a
platform, legal, or commercial claim.

A second opt-in variant, `method_mode:
owner_present_attended_automation_optional_poc_risk` (`optional_poc_risk_mode:
yes`), allows **owner-present attended automation** — the run is automated but
the owner is present at the machine, enforced by a **programmatic presence check
that halts the run if presence lapses.** It binds everything the supervised
variant binds (boundary, caps, minimization, acceptance gate, hard stops
verbatim, `no-entitlement gate bypass` still hard-stopped, stop-on-friction /
person-data-drift). Recorded caveat: a presence check proves presence, not
per-action supervision, and does not make automated access ToS-compliant;
truly-unattended (no owner present) operation stays a hard stop.

## Pilot Closeout Shape

```yaml
pilot_closeout:
  run_id:
  mode: pilot_no_live_operator_supplied_observations | supervised_browser_assist_optional_poc_risk
  declared_theme_or_decision_context:
  candidate_classes:
  source_surfaces_used:
  caps_applied:
  watch_window_or_none:
  row_counts:
    business_org_candidates:
    public_professional_actor_candidates:
    senior_decision_maker_candidates:
    graph_frontier_nodes:
    graph_frontier_edges:
  stop_reason:
  output_artifacts:
    json_or_md_path:
    receipt_path:
  forbidden_output_checks:
    profile_body_absent:
    content_absent:
    contact_fields_absent:
    follower_connection_commenter_list_absent:
    org_chart_or_employment_graph_absent:
    lead_list_absent:
    source_capture_packet_absent:
    data_capture_handoff_absent:
  person_row_checks:
    every_person_has_public_actor_basis:
    every_person_minimized_and_flagged:
  operator_decision:
    recommend_open_promotion_gate: yes | no | deferred   # a planning recommendation ONLY — never promotion itself
    reason:
  non_claims:
    - not live LinkedIn access unless the POC-risk variant was explicitly opted into
    - not contact acquisition, lead list, or follower/connection/commenter graph
    - not Source Capture Packet output, Data Capture handoff, or Outreach Lane execution
    - not commercial use, validation, or readiness
```

The operator decision is a **planning** decision only — it records whether to
*open* the separate promotion gate, never a promotion. Actual promotion is
invalid unless the separate authority-required promotion receipt (§Promotion
Decision) exists.

## Next Authorized Step

Next authorized step: supply the pilot parameters for one
`pilot_no_live_operator_supplied_observations` run —

1. `declared_theme_or_decision_context`;
2. narrowed `candidate_classes` and `source_surface_allowlist` (discoverable/entitled only);
3. operator-supplied seed list / saved notes / observations;
4. caps if lower than the `probe` defaults;
5. whether a bounded watch window is in scope (default: none);
6. stop condition to record if no candidates are emitted.

After those are supplied, a no-live pilot may be run by rowing the supplied
observations into candidate rows + a Graph Frontier register, then writing the
pilot closeout. Live or supervised-browser-assist execution remains separately
gated (the POC-risk variant). No implementation, capture, promotion, commit, or
push is authorized by this plan.

## Non-Claims

This plan is not validation, readiness, source-access boundary amendment, legal
sufficiency, implementation execution, live LinkedIn authorization, supervised
browser-assist authorization (default), no-entitlement gate bypass
authorization, contact acquisition authorization, lead-list authorization,
follower/connection/commenter graph authorization, Source Capture Armory
execution, Source Capture Packet generation, Data Capture handoff, ECR,
Cleaning, Judgment, source-quality scoring, fixture admission, buyer proof,
commercial-use permission, Outreach Lane authorization, storage, scheduler,
dashboard, deployment, production runtime, commit authorization, push
authorization, or PR authorization.
