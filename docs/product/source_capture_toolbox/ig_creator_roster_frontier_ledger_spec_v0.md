# IG Creator Roster And Frontier Ledger Spec v0

```yaml
retrieval_header_version: 1
artifact_role: proposed_source_capture_toolbox_spec
artifact_name: ig_creator_roster_frontier_ledger_spec_v0
status: PROPOSED_LEDGER_SPEC_V0
owner_adoption_required: true
scope: >
  Proposed docs-only ledger contract for an Instagram beauty creator roster,
  public display-name observations, roster lifecycle events, and bounded frontier
  discovery provenance. This is not capture machinery, not a crawler, not a
  runtime schema migration, and not an ontology amendment.
use_when:
  - Designing or reviewing the first durable creator roster ledger for beauty creator monitoring.
  - Deciding what public creator identity fields may be stored and how name changes are preserved.
  - Separating roster entries from frontier discovery candidates before any capture tooling exists.
  - Checking whether a proposed creator roster design remains ontology-compatible without inventing new ontology types.
do_not_use_when:
  - Authorizing scraping, passive discovery, scheduling, account operation, outreach, or capture execution.
  - Defining source capture packet schemas, venue cards, ECR/Cleaning/Judgment behavior, or public product surfaces.
  - Amending the adopted ontology backbone or changing WindCaller doctrine.
open_next:
  - docs/product/core_spine/orca_ontology_backbone_architecture_v0.md
  - docs/product/source_capture_toolbox/ig_creator_discovery_spec_v0.md
  - docs/product/data_capture_spine/orca_creator_monitoring_policy_architecture_v0.md
  - docs/product/data_capture_spine/orca_creator_momentum_pipeline_architecture_v0.md
  - docs/decisions/wind_caller_calibration_carveout_v0.md
  - docs/product/source_capture_toolbox/source_capture_playbook_v0.md
stale_if:
  - The adopted ontology changes the status, definition, or ID grammar for WindCaller, SubNiche, Observation, CapturePacket, TrendVector, or DecisionEvent.
  - Wind-caller calibration doctrine changes public-name, subject-roster, passive-monitoring, or exclusion boundaries.
  - The IG creator discovery spec changes the allowed discovery posture, depth model, or roster-output contract.
  - A runtime implementation schema is adopted that supersedes this proposed docs-only contract.
authority_boundary: retrieval_only
```

## Start Preflight

```yaml
orca_start_preflight:
  agents_read: true
  overlay_read: true
  cynefin_route: complicated_with_complex_edge
  source_pack: custom_s3_target_deepening
  edit_permission: docs_write_default_allowed
  isolation: worktree_off_origin_main
  worktree: .codex/worktrees/beauty-creator-roster-ledger
  dirty_state_checked: true
  target_scope: >
    Write a proposed non-authorizing ledger spec for the beauty creator roster
    and frontier ledger, incorporating the adversarial second opinion while
    preserving the adopted ontology backbone boundary.
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/artifact-folders.md
    - .agents/workflow-overlay/retrieval-metadata.md
    - docs/product/core_spine/orca_ontology_backbone_architecture_v0.md
    - docs/product/source_capture_toolbox/ig_creator_discovery_spec_v0.md
    - docs/product/data_capture_spine/orca_creator_monitoring_policy_architecture_v0.md
    - docs/decisions/wind_caller_calibration_carveout_v0.md
```

## Status

This is a proposed product/source-capture spec. It does not change the adopted
ontology, authorize capture runs, create a database schema, start any monitoring,
or approve a public person-level surface.

The immediate purpose is to lock the smallest complete ledger shape before any
implementation prompt or capture runner can accidentally drift into a crawler,
relationship graph, person dossier, or ontology fork.

## Source Context

Primary sources read for this spec:

- `docs/product/core_spine/orca_ontology_backbone_architecture_v0.md`
- `docs/product/source_capture_toolbox/ig_creator_discovery_spec_v0.md`
- `docs/product/data_capture_spine/orca_creator_monitoring_policy_architecture_v0.md`
- `docs/product/data_capture_spine/orca_creator_momentum_pipeline_architecture_v0.md`
- `docs/decisions/wind_caller_calibration_carveout_v0.md`
- `docs/product/source_capture_toolbox/source_capture_playbook_v0.md`
- `docs/product/source_capture_toolbox/capture_recon_index_v0.md`
- User-supplied adversarial second opinion: `Adversarial Second Opinion - Beauty Creator Roster + Frontier Ledger`

Relevant source facts:

- The ontology backbone is adopted for a bounded core set and owns names,
  definitions, links, action gates, and ID grammar. It does not freeze property
  lists for operational ledgers.
- `WindCaller` is an adopted ontology object type. The ontology source does not
  currently define a first-class `Creator` object type.
- The creator momentum pipeline treats platform identifiers as stable and
  usernames as mutable, and keeps discovery/deep-capture platform knowledge in
  satellite/source-capture layers rather than hard-binding it to core ontology
  objects.
- The monitoring policy allows A/B/C roster tiering and hot-list behavior, but
  forbids drift into a standing crawler or unattended discovery system.
- The wind-caller carve-out allows public handles and public names for
  calibration subjects, while excluding contact data, private/non-public data,
  special-category data, outreach lists, resale/data-broker use, and external
  person-level surfaces.

## Review Disposition

The adversarial second opinion is accepted with one ontology correction.

Accepted findings:

- Name storage must be append-only observations, not a single mutable field.
- Frontier records must be discovery provenance, not a relationship graph.
- v0 must cap discovery at depth 1 and prevent candidates from becoming
  automatic seeds.
- Privacy boundaries must be schema invariants, not optional policy prose.
- `disposition_reason` is clearer than `rejection_or_revisit_reason`.
- The first proof slice should be denser and smaller than a broad 1,000-creator
  all-beauty roster.

Corrected finding:

- The review framed `Creator` as the first-class ontology object and
  `WindCaller` as only a status. That is not compatible with the adopted
  ontology source. In this spec, creator records are ledger-local operational
  records. A creator record may later be mapped to an ontology `WindCaller` only
  if it satisfies the separate wind-caller calibration rules. This spec creates
  no new ontology `Creator` object type.

## Core Decision

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

The roster should start with one or two high-density beauty sub-niches and
roughly 300 to 500 rostered entries. A broad 1,000-creator beauty roster remains
a later scale target after the loop proves useful in a bounded sub-niche.

This is product sequencing, not a legal cap. The wind-caller carve-out does not
cap the number of public subject creators that may be considered, but the first
durable ledger should not lock in broad, low-density coverage before the
promotion, review, and safety loop is proven.

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
- It must not be cross-platform stitched without a separate owner-approved spec.

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

- Every run must have an owner gate before execution.
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
- Email, phone, DM handle beyond the public platform handle, contact form, media
  kit contact, or outreach field.
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
- Any frontier candidate name without source pointer and source field is invalid.
- Contact fields should not exist in the schema.
- Demographic fields should not exist in the schema.
- Relationship/current-graph fields should not exist in the schema.
- Scheduling fields must be advisory only and must not self-execute.

## Tiering And First Slice

Initial proof slice:

- One or two beauty sub-niches.
- 300 to 500 rostered creator records.
- All entries must be placed into A/B/C monitoring priority.
- At least 100 entries should be reviewed deeply enough to validate name
  observation, sub-niche assignment, tiering, and lifecycle event behavior.
- Frontier rows may exceed roster rows, but must remain depth-1 provenance.

Suggested tier distribution for the first proof slice:

- Tier A: 30 to 50 high-relevance, high-signal records.
- Tier B: 90 to 150 useful recurring references.
- Tier C: remaining long-tail context, parked for low-touch review.

Later scale target:

- A 1,000-creator all-beauty roster can be reconsidered only after the first
  slice proves that name observations, promotion, demotion, frontier disposition,
  and privacy invariants hold under real operator use.

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

## Acceptance Checks For A Future Implementation Prompt

A downstream implementation prompt may use this spec only if it preserves these
checks:

- It uses append-only name observations.
- It keeps roster current-name fields as caches derived from observations.
- It rejects name rows without source pointer and source field.
- It rejects contact, demographic, private, inferred, or cross-platform identity
  fields.
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

## Open Questions

- Which first beauty sub-niche should be used for the proof slice?
- What coarse follower bands should v0 allow?
- Which source pointer grammar should be canonical for IG public profile reads?
- Should a later implementation represent these records as YAML fixtures,
  SQLite tables, or a typed Python data model first?
- What owner gate is required before any actual attended discovery run?

## Recommendation

Adopt this as the next non-authorizing spec shape before writing any
implementation prompt. The first implementation prompt should target only a
static ledger model or fixture validator for one bounded sub-niche, not capture
execution.

Do not proceed to broad 1,000-creator coverage until the bounded slice proves
that name history, frontier disposition, roster lifecycle movement, and privacy
invariants work together without creating a person dossier or current
relationship graph.
