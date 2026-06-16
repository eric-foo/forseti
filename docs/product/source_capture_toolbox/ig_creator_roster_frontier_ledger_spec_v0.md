# IG Creator Roster And Frontier Ledger Spec v0

```yaml
retrieval_header_version: 1
artifact_role: proposed_source_capture_toolbox_spec
scope: >
  Proposed current-main ledger contract for an Instagram beauty creator roster,
  append-only public display-name observations, roster lifecycle events, and
  bounded frontier discovery provenance. This is not capture machinery, not a
  crawler, not a runtime schema migration, and not an ontology amendment.
use_when:
  - Designing or reviewing the first durable beauty creator roster/frontier ledger.
  - Separating current-main roster sizing and commercial target facts from old branch residue.
  - Checking whether a proposed creator roster design preserves privacy and ontology boundaries.
open_next:
  - docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md
  - docs/product/data_capture_spine/orca_creator_monitoring_policy_architecture_v0.md
  - docs/product/source_capture_toolbox/ig_at_scale_operating_envelope_v0.md
  - docs/decisions/wind_caller_calibration_carveout_v0.md
branch_or_commit: 45c6fac9
stale_if:
  - The first commercial beauty target, proof decision family, or buyer-proof boundary changes.
  - The IG monitoring policy changes the roster gates, serious-v0 planning target, or A/B/C allocation.
  - Wind-caller calibration doctrine changes public-name, subject-roster, passive-monitoring, or exclusion boundaries.
  - The adopted ontology changes the status of WindCaller, SubNiche, Observation, CapturePacket, TrendVector, or DecisionEvent.
  - A runtime implementation schema is adopted that supersedes this proposed docs-only contract.
authority_boundary: retrieval_only
```

## Start Preflight

```yaml
orca_start_preflight:
  agents_read: true
  overlay_read: true
  cynefin_route: complicated
  source_pack: custom_s3_target_deepening
  edit_permission: docs_write
  isolation: existing_successor_worktree_off_origin_main
  worktree: .codex/worktrees/beauty-creator-commercial-target-successor
  branch: codex/beauty-creator-commercial-target-successor
  head_confirmed: 45c6fac9
  origin_main_confirmed_after_fetch: 45c6fac9
  dirty_state_checked: true
  target_scope: >
    Port only the old roster-ledger branch's still-useful ledger, privacy, and
    frontier semantics into a proposed current-main source-capture spec, while
    aligning roster sizing and commercial target facts to current main.
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md
    - docs/product/product_lead/orca_offer_hypothesis_v0.md
    - docs/product/product_lead/orca_buyer_proof_packet_v0.md
    - docs/product/product_lead/orca_discovery_consumer_demand_target_selection_brief_v0.md
    - docs/product/data_capture_spine/orca_creator_monitoring_policy_architecture_v0.md
    - docs/product/source_capture_toolbox/ig_at_scale_operating_envelope_v0.md
    - docs/decisions/wind_caller_calibration_carveout_v0.md
```

## Status

This is a proposed product/source-capture spec. It does not change the adopted
ontology, authorize capture runs, create a database schema, start any
monitoring, approve outreach, or approve a public person-level surface.

The immediate purpose is to preserve the smallest complete ledger shape before
any implementation prompt or capture runner can drift into a crawler,
relationship graph, person dossier, stale proof-slice sizing, or ontology fork.

## Source Context

Current-main sources read for this spec:

- `docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md`
- `docs/product/product_lead/orca_offer_hypothesis_v0.md`
- `docs/product/product_lead/orca_buyer_proof_packet_v0.md`
- `docs/product/product_lead/orca_discovery_consumer_demand_target_selection_brief_v0.md`
- `docs/product/data_capture_spine/orca_creator_monitoring_policy_architecture_v0.md`
- `docs/product/source_capture_toolbox/ig_at_scale_operating_envelope_v0.md`
- `docs/decisions/wind_caller_calibration_carveout_v0.md`
- `docs/product/core_spine/orca_ontology_backbone_architecture_v0.md`
- `docs/product/source_capture_toolbox/ig_creator_discovery_spec_v0.md`
- `docs/product/data_capture_spine/orca_creator_momentum_pipeline_architecture_v0.md`
- `docs/product/source_capture_toolbox/source_capture_playbook_v0.md`

Old-branch context read:

- `codex/beauty-creator-roster-ledger:docs/product/source_capture_toolbox/ig_creator_roster_frontier_ledger_spec_v0.md`

That old branch is orientation only. The old branch's unique ledger semantics
are ported here only where compatible with current main. Its old single-gate
500-record proof-slice target is not ported as controlling current truth.

## Current-Main Alignment

Current controlling facts for this spec:

- First commercial target: US-market tractioned indie/DTC beauty or
  personal-care operators with a named founder, head of brand, growth,
  insights, strategy, or equivalent decision owner facing a live 30-90 day
  demand-allocation decision.
- First decision-family bias: retail/channel expansion, launch/reposition, and
  inventory or purchase-depth commitment.
- Current beauty-first IG roster gates: `250 -> 500 -> 1,000`.
- Current serious-v0 planning target: 1,000 creators with 10/30/60 A/B/C
  allocation.
- The 1,000-creator path is a non-authorizing operating envelope. It is not
  live capture, proxy purchase, session/cookie wiring, scheduler/runtime work,
  network configuration, or commercial-scale collection.

Retailer/category teams are not the first buyer door. Agencies and incubators
may later help route to accountable brand decision owners, but their interest
alone is not buyer proof. Buyer/company outreach lists are separate from this
creator roster.

## Reconciliation Decision

Build the first durable artifact as a ledger-local roster and frontier
provenance contract:

- `creator_roster_entry`: the current operational roster row.
- `creator_name_observation`: append-only public display-name history.
- `roster_lifecycle_event`: append-only movement, tier, and state history.
- `frontier_adjacency_observation`: append-only depth-1 discovery provenance.
- `discovery_run_receipt`: receipt interface for bounded attended discovery
  runs, not run machinery.
- `candidate_promotion_link`: append-only bridge from frontier candidate to
  roster entry when a candidate is promoted.

This spec keeps the old branch's still-useful ledger/privacy/frontier
semantics:

- public names are append-only observations, not mutable facts;
- any stored name requires a source pointer and source field;
- privacy exclusions are schema invariants, not optional prose;
- frontier records are provenance observations, not a current relationship
  graph;
- v0 frontier depth is 1;
- candidates never become automatic seeds;
- promotion preserves a link from frontier provenance to roster entry;
- `creator_record_id` is ledger-local;
- `ontology_windcaller_id` is nullable and separately earned;
- no `Creator` ontology type is created.

## Commercial Slice And Roster Gates

The first roster should be commercially coherent before it is broad. Use one
beauty sub-niche, or two tightly adjacent sub-niches only if the same qualified
buyer decision truly needs both.

Use the current main gates:

| Gate | A | B | C | Purpose |
| --- | ---: | ---: | ---: | --- |
| 250 | 25 | 75 | 150 | Ledger/provenance shakeout on one commercially coherent slice. |
| 500 | 50 | 150 | 300 | Second gate after name, frontier, lifecycle, and privacy behavior survive operator use. |
| 1,000 | 100 | 300 | 600 | Current serious-v0 planning target for the beauty-first IG path. |

The gate counts use the current 10/30/60 A/B/C allocation. They are planning
defaults, not validation proof and not capture authorization.

Tier meaning:

- Tier A: dense monitoring for rising/high-signal creators and current
  breakouts.
- Tier B: sampled monitoring for established or slower creators.
- Tier C: cheap heartbeat so the known vertical stays on the radar.
- Hot-list: floating temporary attention while a spike persists.

Do not read the 500 gate as the final target, and do not jump to 1,000 before
the 250 and 500 gates demonstrate that roster identity, public-name
observations, lifecycle movement, frontier disposition, and privacy invariants
work together without creating a person dossier or current relationship graph.

## Identity Model

### Ledger-Local Creator Record

`creator_record_id` is a ledger-local stable identifier minted only when a
candidate is promoted into the roster. It is not an ontology ID.

Required behavior:

- It survives handle changes and public display-name changes.
- It is keyed primarily by stable platform ID where the source exposes one.
- It may use normalized handle as a fallback only when stable platform ID is
  unavailable, with the limitation recorded.
- It must not be exposed as proof that the person is a real-world identity.
- It must not be cross-platform stitched without a separate owner-approved
  spec.

### Public Name

The roster may cache a current public display name for usability, but the cache
is derived from the latest valid `creator_name_observation`.

Allowed:

- Public profile display name observed on an allowed public surface.
- Public handle.
- Platform-local public account ID or stable platform identifier.

Forbidden:

- Legal name.
- Real name inferred from off-platform sources.
- Derived or guessed name.
- Name from private, auth-gated, leaked, purchased, or contact-enrichment
  sources.
- Any field whose purpose is to identify or contact the person outside the
  public creator surface.

### Name Source Pointer

A name source pointer is the receipt pointer showing exactly where the public
display name was observed.

Example shape:

```yaml
name_source_pointer: source_capture_packet:ig:web_profile_info:2026-06-16:dieuxskin
name_source_field: data.user.full_name
name_observed_at: 2026-06-16T10:45:00Z
```

Both `name_source_pointer` and `name_source_field` are required for any stored
display-name observation. If the source pointer or source field is missing, the
name must not be stored.

## Ontology Boundary

This spec is ontology-compatible, not ontology-authoritative.

Ledger concepts:

- `creator_record_id`: local roster ID.
- `candidate_platform_id`: local frontier dedupe key.
- `tier`: roster monitoring priority.
- `signal_state`: operational state used by source capture and monitoring.
- `disposition`: frontier or lifecycle outcome.

Ontology concepts used by pointer or adapter:

- `SubNiche`: classification target for beauty sub-niche.
- `WindCaller`: adopted ontology object type for qualified signal-bearing
  referents.
- `Observation`: external observation concept referenced by source pointers.
- `CapturePacket`: source evidence packet referenced by source pointers.
- `TrendVector`: downstream trend signal that may consume roster observations.
- `DecisionEvent`: owner-visible promotion or action event when acted on.

Mapping rules:

- Ordinary roster entries do not become ontology objects by default.
- Frontier candidates never receive ontology IDs.
- `ontology_windcaller_id` is nullable and may be set only when a roster entry
  is separately accepted as a `WindCaller` referent.
- A `WindCaller` mapping does not erase the ledger-local history. The ledger
  remains the backing operational evidence trail.
- This spec does not create a `Creator` ontology type.
- This spec does not amend ontology folders, routers, IDs, definitions, or link
  grammar.

## Roster Entry Contract

`creator_roster_entry` is the current operational roster row. It exists to let
operators and later tooling decide who belongs in the monitoring roster, what
sub-niche they represent, and what review cadence is appropriate.

Suggested fields:

```yaml
creator_roster_entry:
  creator_record_id: required stable ledger-local id
  platform: required enum, v0 ig only
  platform_creator_id: preferred stable public platform id when available
  handle: required public handle at time of latest roster refresh
  handle_observed_at: required timestamp
  handle_source_pointer: required source pointer
  current_public_display_name: nullable cache from latest valid name observation
  current_name_observed_at: nullable timestamp from latest valid name observation
  primary_sub_niche: required ontology-compatible sub-niche label or pointer
  secondary_sub_niches: optional bounded list
  follower_band: optional coarse band, never exact count in v0
  market_role_label: optional cited public role label
  market_relevance_reason: required short rationale
  roster_tier: required enum A, B, C
  roster_status: required enum active, paused, parked, removed
  signal_state: required enum rostered, windcaller_candidate, windcaller_active, not_signal_bearing
  ontology_windcaller_id: nullable ontology pointer
  inclusion_source_pointer: required source pointer
  inclusion_reason: required short text
  limitation_note: optional short text
  last_checked_at: nullable timestamp
  next_due_at: nullable advisory timestamp, never self-firing
  created_at: required timestamp
  updated_at: required timestamp
```

Field invariants:

- `creator_record_id` is minted only at roster promotion.
- `current_public_display_name` is a cache, not the source of truth.
- `primary_sub_niche` must be ontology-compatible, but this ledger does not own
  the sub-niche taxonomy.
- `roster_tier` is monitoring priority, not importance, truth, or quality.
- `signal_state` is operational status. It does not override the ontology.
- `next_due_at` is advisory only. It must not imply an autonomous scheduler.

## Name Observation Contract

`creator_name_observation` is append-only.

Suggested fields:

```yaml
creator_name_observation:
  name_observation_id: required stable ledger-local id
  creator_record_id: required roster id
  observed_public_display_name: required public string
  observed_at: required timestamp
  name_source_pointer: required source pointer
  name_source_field: required source field
  platform: required enum, v0 ig only
  handle_at_observation: required public handle
  observation_posture: required enum public_profile, public_post, public_other
  actor: required operator or system lane id
  created_at: required timestamp
```

Rules:

- Append a new row when a public display name changes.
- Do not overwrite prior rows.
- The roster cache may update to the latest valid observation.
- If the display name disappears or is unavailable, record no new name unless a
  public source explicitly shows the replacement value.
- Do not infer continuity of real-world identity from a name change alone.

## Roster Lifecycle Event Contract

`roster_lifecycle_event` is append-only. It records why a roster row changed.

Suggested fields:

```yaml
roster_lifecycle_event:
  roster_event_id: required stable ledger-local id
  creator_record_id: required roster id
  event_type: required enum
  from_value: nullable prior state
  to_value: nullable new state
  event_reason: required short text
  evidence_pointer: required source pointer or review packet pointer
  metric_snapshot_pointer: nullable pointer
  actor: required operator or system lane id
  occurred_at: required timestamp
```

Allowed `event_type` values for v0:

- `promoted_to_roster`
- `tier_changed`
- `status_changed`
- `signal_state_changed`
- `sub_niche_corrected`
- `handle_changed`
- `removed_from_roster`
- `review_note_added`

Rules:

- Lifecycle events explain movement. They are not a capture packet substitute.
- Acting on a promotion may later become an ontology `DecisionEvent`, but this
  ledger does not mint that ontology event.
- Promotion and demotion must preserve old state through event history.

## Frontier Contract

The frontier is discovery provenance. It is not a current-state relationship
graph.

Use `frontier_adjacency_observation`, not a relationship table.

Suggested fields:

```yaml
frontier_adjacency_observation:
  frontier_observation_id: required stable ledger-local id
  discovery_run_id: required receipt id
  source_seed_ref: required roster id or owner-approved seed ref
  source_seed_kind: required enum roster_entry, owner_seed
  platform: required enum, v0 ig only
  candidate_platform_id: preferred stable public platform id when available
  candidate_handle: required public handle
  candidate_public_display_name: nullable public name
  candidate_name_source_pointer: required if candidate_public_display_name is stored
  candidate_name_source_field: required if candidate_public_display_name is stored
  discovery_surface: required enum
  discovery_adjacency_type: required enum
  depth: required integer, v0 must be 1
  first_seen_at: required timestamp
  evidence_pointer: required source pointer
  confidence_label: required enum low, medium, high
  disposition: required enum new, parked, promoted, rejected
  disposition_reason: nullable short text
  created_at: required timestamp
```

Allowed `discovery_surface` values for v0:

- `profile_following_sample`
- `profile_followed_by_sample`
- `tagged_profile`
- `mention_or_credit`
- `comment_visible_public`
- `public_list_or_collection`
- `operator_seed_note`

Allowed `discovery_adjacency_type` values for v0:

- `visible_follow_edge`
- `visible_tag_edge`
- `visible_mention_edge`
- `visible_credit_edge`
- `visible_comment_edge`
- `operator_observed_neighbor`

Rules:

- v0 depth is exactly 1.
- A candidate never becomes an automatic seed.
- Promoting a candidate to a future seed requires a separate owner-gated
  discovery run.
- Dedupe by `(platform, candidate_platform_id)` when available.
- If stable platform ID is unavailable, dedupe by `(platform, normalized_handle)`
  and record the limitation.
- The frontier does not claim a social relationship, endorsement,
  collaboration, influence, or current network state.
- Do not refresh frontier rows into a current graph. Add a new observation if a
  later bounded run sees the candidate again.
- Terminal dispositions are `parked`, `promoted`, and `rejected`.
- `disposition_reason` is required for `rejected` and recommended for `parked`.

## Candidate Promotion Link

`candidate_promotion_link` preserves the bridge between frontier provenance and
the roster entry created from it.

Suggested fields:

```yaml
candidate_promotion_link:
  promotion_link_id: required stable ledger-local id
  frontier_observation_id: required frontier observation id
  creator_record_id: required new or existing roster id
  promoted_at: required timestamp
  promotion_reason: required short text
  actor: required operator or system lane id
```

Rules:

- Promotion does not mutate the frontier row into a roster row.
- Promotion mints `creator_record_id` only if no matching roster entry already
  exists.
- Prior frontier observations for the same candidate should be linked or
  suppressed from re-promotion review.

## Discovery Run Receipt Interface

`discovery_run_receipt` is a receipt contract for bounded attended discovery.
It is not a scheduler, crawler, or runner.

Suggested fields:

```yaml
discovery_run_receipt:
  discovery_run_id: required stable ledger-local id
  run_kind: required enum manual_attended, bounded_operator_assisted
  owner_gate_pointer: required approval or prompt pointer
  seed_set_pointer: required pointer to seed list
  commercial_slice_pointer: required buyer-decision or sub-niche scope pointer
  sub_niche_scope: required bounded sub-niche label or pointer
  read_cap: required integer
  depth_cap: required integer, v0 default and max 1
  start_time: required timestamp
  end_time: required timestamp
  stop_reason: required enum cap_reached, operator_stopped, source_blocked, no_more_relevant_candidates
  candidate_count_seen: required integer
  candidate_count_new: required integer
  candidate_count_promoted: required integer
  candidate_count_parked: required integer
  candidate_count_rejected: required integer
  limitations: required short text
  non_claims: required short text
```

Rules:

- This spec does not authorize any run.
- Every run needs a separate owner gate before execution.
- Every run must terminate.
- A receipt may report block, empty, or low-yield outcomes. These are valid
  outcomes, not failures to hide.
- No receipt can authorize future passive discovery.
- No receipt can widen the depth cap without a new spec or owner decision.

## Privacy And Safety Invariants

Allowed in v0:

- Public handle.
- Public display name with source pointer and source field.
- Public platform-local ID or stable platform identifier.
- Coarse follower band.
- Public market role label when cited to an allowed public source.
- Sub-niche label or pointer.
- Roster tier and operational status.
- Discovery provenance pointer.
- Lifecycle movement reason.
- Limitations and non-claims.

Forbidden in v0:

- Legal name or inferred real name.
- Exact location, home city, address, travel pattern, or venue attendance
  pattern.
- Email, phone, DM handle beyond the public platform handle, contact form,
  media kit contact, or outreach field.
- Age, gender, ethnicity, health, religion, politics, sexuality, family status,
  or other demographic/special-category data.
- Exact follower count when a coarse band is sufficient.
- Employer, school, agency, or management details unless separately approved as
  public brand/business context for a non-person entity.
- Cross-platform identity stitching.
- Private, auth-gated, purchased, leaked, or enriched data.
- Resale, lead-list, data-broker, outreach, or targeting use.
- Public person-level product surface.

Schema-level enforcement expectations:

- Any name row without `name_source_pointer` and `name_source_field` is invalid.
- Any frontier candidate name without source pointer and source field is
  invalid.
- Contact fields should not exist in the schema.
- Demographic fields should not exist in the schema.
- Relationship/current-graph fields should not exist in the schema.
- Scheduling fields must be advisory only and must not self-execute.

## Non-Goals

This spec does not:

- Build a database.
- Build a runner.
- Start a monitoring job.
- Start a crawler.
- Authorize scraping.
- Authorize passive discovery.
- Define source capture packet schemas.
- Define venue cards.
- Define ECR, Cleaning, Judgment, or downstream scoring.
- Create outreach lists.
- Create commercial lead lists.
- Create a public creator directory.
- Change ontology.
- Mint a `Creator` ontology type.
- Decide that any roster entry is a `WindCaller`.
- Claim buyer proof, validation, readiness, adoption, or commercial usefulness.

## Acceptance Checks For A Future Implementation Prompt

A downstream implementation prompt may use this spec only if it preserves these
checks:

- It uses append-only name observations.
- It keeps roster current-name fields as caches derived from observations.
- It rejects name rows without source pointer and source field.
- It rejects contact, demographic, private, inferred, or cross-platform
  identity fields.
- It keeps frontier rows append-only and provenance-only.
- It uses `discovery_adjacency_type`, not `relationship_type`.
- It caps v0 depth at 1.
- It prevents automatic candidate-as-seed behavior.
- It uses `disposition` and `disposition_reason`.
- It treats `creator_record_id` as ledger-local, not ontology ID.
- It maps to ontology `WindCaller` only through a nullable pointer after
  separate acceptance.
- It preserves failed, blocked, and empty discovery receipts.
- It includes explicit non-claims in run receipts and review outputs.
- It uses current-main roster gates `250 -> 500 -> 1,000`, not the old
  branch's 500-record target as final current truth.

## Open Questions

- Which first commercial beauty sub-niche and live buyer decision should anchor
  the 250-record first gate?
- What coarse follower bands should v0 allow?
- Which source pointer grammar should be canonical for IG public profile reads?
- What owner gate is required before any actual attended discovery run?
- Should a later implementation represent these records as YAML fixtures,
  SQLite tables, or a typed Python data model first?

## Recommendation

Use this as the current-main proposed ledger shape before writing any
implementation prompt. The first implementation prompt, if later authorized,
should target only a static ledger model or fixture validator for one bounded
commercially coherent sub-niche, not capture execution.

Do not proceed to broad 1,000-creator coverage until the earlier gates prove
that name history, frontier disposition, roster lifecycle movement, and privacy
invariants work together without creating a person dossier or current
relationship graph.
