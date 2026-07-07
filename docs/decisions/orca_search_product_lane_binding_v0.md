# Orca Search Product Lane Binding v0

```yaml
retrieval_header_version: 1
artifact_role: Orca decision record
scope: >
  Binds `search/` as a docs/product/ lane: Orca's search / answer-engine
  surfaces PLUS the demand-signal discovery method (scan, read-grammar, gates)
  those surfaces feed. Holds the lane inclusion test + precedence rule and
  references the migration package that physically co-locates the member docs.
  Extends the docs/product/ by-lane parameter bound in
  docs/decisions/forseti_repo_structure_binding_v0.md.
use_when:
  - Deciding whether a doc belongs in docs/product/search/ versus a spine lane.
  - Authoring or revising repo-structure.yaml product_lanes or artifact-folders.
  - Planning or executing the search-lane migration.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_spine_first_blocker_authorization_v0.md
  - docs/decisions/forseti_repo_structure_binding_v0.md
  - .agents/workflow-overlay/artifact-folders.md
  - repo-structure.yaml
  - docs/migration/repo_structure_search_lane_v0/runbook.md
  - docs/product/search/README.md # nonresolving: retired without successor; resolve via docs/migration/repo_structure_spine_first_v0/moved_paths_index.md
stale_if:
  - repo-structure.yaml and this record disagree on the search lane or its status.
  - A later accepted Orca decision supersedes the lane, its inclusion test, or its precedence rule.
```

## Status

Owner-authorized adoption, v0. Created and EXPANDED in one session, before the
lane landed on main (PR #236, unmerged): a first move co-located the 4
search/answer-engine-surface docs ("full physical move", option C); the owner
then directed completing the migration to the demand-signal discovery method
("we have to make expansion; indexing is just a crutch ... preserve integrity"),
expanding the move by +6 demand-scan/read/gate docs and excluding 3 non-search
docs. Reached through deep-think -> assumption-gate -> re-scope ->
implementation-scoping -> micro-decision-lock, each step owner-confirmed. This
binds the lane as Orca doctrine; it is not validation, readiness, or product
proof.

Spine-first supersession note (2026-06-18): the lane remains the current
physical home until the spine-first migration executes, but
`docs/decisions/forseti_spine_first_blocker_authorization_v0.md` confirms that
future spine-first placement supersedes this record's physical
`docs/product/search/` home and topic-primacy precedence. The demand-signal
method docs keep their venue-spanning authority; only the physical home changes
during execution.

Spine-first Wave B note (2026-06-18): execution has begun. The 11 `search/` docs
dissolve by spine function in Wave C (scan-core -> `scanning/scan_core/`; gate
docs -> `scanning/admissibility_checkability/` + `commission_signal_board/dispatch_rules/`;
taxonomy -> `foundation/demand_read_taxonomy/`; AEO -> `scanning/source_families/answer_engine/`;
search-interest profile -> `capture/demand_durability_indicators/search_interest/`).
`docs/product/search/README.md` is **RETIRED with no successor** (the lane front
door is superseded by the spine-first binding + the moved-paths index); its one
durable asset — the cross-spine consumer/dependency map — is reseeded natively as
bidirectional pointers in the new structure (`foundation/demand_read_taxonomy`,
`scanning`, `capture/source_families/answer_engine`, `judgment/demand_read`), not
carried over. Recorded as a search-dissolution line item; handled in Wave C/E.

## Decision

`docs/product/search/` is a bound second-level lane under `docs/product/`,
extending the by-lane axis bound in
`docs/decisions/forseti_repo_structure_binding_v0.md`. It is Orca's **demand-signal
intelligence (search-led)** vertical, holding two coherent things:

1. **Search / answer-engine surfaces** - how Orca captures, reads, and
   source-classes search-surface and answer-engine signal (web search / SERP,
   Google AI Overviews and other answer engines, zero-click, AEO/GEO,
   search-interest / "trends").
2. **The demand-signal discovery method** those surfaces feed - the scan method,
   the demand-read grammar/taxonomy, and the demand gates that adjudicate
   discovered signal.

This lane is a deliberate **topic** vertical beside the function (spine) lanes
(see "Relationship to invariant #1"). The method docs (item 2) are search-led
but **venue-spanning**: they govern demand reads across all venues and are
consumed by the judgment, data-capture, and core spines. They live here because
the search/trends lane owns demand-signal discovery, not because they are
search-only; their cross-spine references resolve into `docs/product/search/`.

## Inclusion test (bound)

A doc belongs in `docs/product/search/` when its reason-to-exist is either:

- (a) the **search / answer-engine surface** itself - how Orca captures it, what
  it exposes, or its source-class; OR
- (b) the **demand-signal discovery method** that drives those reads - the scan
  method, the demand-read grammar/taxonomy, or the demand gates that adjudicate
  discovered signal.

It excludes a doc whose primary subject is a different venue's capture (retail
price / availability / reviews, or Reddit HTML intake), or a one-shot data
handoff / discovery research artifact, even when it touches search.

## Precedence rule (bound)

When a doc is both in-scope here and spine-functional, topic-primacy wins: it
lives in `search/`, not its spine lane. Every artifact keeps exactly one
physical home (invariant #6); there is no dual placement.

## Scope - what this lane holds (v0)

Move-set (physically relocated by the migration package).

Search / answer-engine surfaces:

| New home `docs/product/search/` | Moved from |
| --- | --- |
| `aeo_capture_feasibility_probe_phase0_v0.md` | `source_capture_toolbox/` |
| `aeo_capture_feasibility_probe_phase0_v0_evidence.json` | `source_capture_toolbox/` |
| `demand_search_interest_sourcing_and_gate_delta_spec_v0.md` | `data_capture_spine/` |
| `demand_durability_indicator_search_interest_capture_profile_v0.md` | `data_capture_spine/` |

Demand-signal discovery method (search-led, venue-spanning):

| New home `docs/product/search/` | Moved from |
| --- | --- |
| `orca_demand_scan_core_spec_v0.md` | `core_spine/` |
| `orca_demand_read_taxonomy_v0.md` | `product_lead/` |
| `orca_demand_read_taxonomy_adjudication_v0.md` | `product_lead/` |
| `orca_demand_scan_gate_adjudication_packet_v0.md` | `product_lead/` |
| `orca_demand_gate_definition_closures_proposal_v0.md` | `product_lead/` |
| `orca_demand_gate_run_commission_criteria_v0.md` | `product_lead/` |

Explicitly EXCLUDED (touches search but out of scope - moving them would
mislabel them):

- the retail availability/restock, price-timeseries, and review-velocity
  durability capture profiles (`data_capture_spine/`) - different venues;
- `reddit_candidate_intake_old_reddit_search_surface_handling_v0.md`
  (`workflows/`) - old-Reddit HTML parsing, not search-interest;
- `consumer_demand_candidate_pool_handoff_v0.md` (`core_spine/`) - a one-shot
  candidate roster, not method;
- `orca_discovery_candidate_scan_beauty_neutral_chatgptpro_v0.md` (`research/`) -
  a discovery research artifact.

The inclusion test governs future membership; this scope is not exhaustive of
what may later qualify.

## Relationship to invariant #1 (one primary axis per subtree)

The `docs/product/` axis is otherwise by spine-function. `search/` is a topic
axis, so adding it beside the spine lanes bends invariant #1 - and the expansion
to the demand-signal method docs bends it further, since those foundations are
consumed across the judgment, capture, and core spines yet now live in the topic
lane. The owner accepted this trade deliberately ("indexing is just a crutch; we
have to make expansion") for a long-term demand-signal vertical, with an explicit
"preserve integrity" instruction. It is contained, not waived: the inclusion
test bounds membership to search-surface + demand-signal-discovery-method (not
the whole demand spine), the precedence rule preserves invariant #6 (single
physical home), and the moved foundations keep their cross-spine references
(which now resolve into `search/`). Any further topic vertical or lane expansion
is a deliberate extension recorded by its own decision, not an open licence.

## Migration (packaged + applied on the lane branch)

The physical co-location is packaged under
`docs/migration/repo_structure_search_lane_v0/` (10-row manifest, dedicated
idempotent apply/reverse script, runbook, reference inventory, moved-paths
index). The apply engine scans and rewrites all live references (the expansion
touches ~19 live files across judgment_spine / data_capture_spine / core_spine /
product_lead) and preserves git history via `git mv`. Historical records keep
their old paths and resolve via the moved-paths index. The owner authorized
applying it on the lane branch and committed to not reopening the contended
spines during the window; `repo-structure.yaml` carries `search` at
`status: current` once applied.

## Controlling sources updated by this change

- `repo-structure.yaml` - `product_lanes` += `{ name: search }` (current once applied).
- `.agents/workflow-overlay/artifact-folders.md` - search-lane accepted-folder entry + lane-subfolder list + the direction-change-propagation receipt.
- `docs/decisions/forseti_repo_structure_binding_v0.md` - bound-lanes bullet notes `search/`.
- `docs/product/README.md` - lane list includes `search/`.
- `docs/product/search/README.md` - lane front-door index.
- `docs/workflows/orca_repo_map_v0.md` - Workstream Status Pointers row.
- `docs/migration/repo_structure_search_lane_v0/` - the migration package (manifest, apply/reverse script, runbook, reference inventory, moved-paths index).
- The 10 moved docs (search / answer-engine surfaces + demand-signal method) and the ~19 live referencing files whose paths the apply rewrites.

## Direction change propagation

The `direction_change_propagation` receipt for this change set lives inline in
`.agents/workflow-overlay/artifact-folders.md` (a controlling overlay source
updated), per the Doctrine Change Propagation Contract in
`.agents/workflow-overlay/source-of-truth.md`.

## Non-claims

- Not validation, readiness, approval, or product proof; placement / doctrine only.
- Placement of the demand-signal method docs in `search/` does not narrow their
  authority: they remain venue-spanning demand foundations, not search-only.
- Not a ToS, legal, or sourcing authorization; the AEO probe's own posture and
  non-claims are unchanged by relocation.
- A green `check_placement.py` run after apply is placement shape, not validation
  or authority (placement is not authority).
