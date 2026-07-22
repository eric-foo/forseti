# Reddit Subreddit Registry Lake Cut-Over Architecture (Proposal v0)

```yaml
retrieval_header_version: 1
artifact_role: source_capture_family_architecture_contract
scope: >
  Proposed architecture for moving live Reddit Subreddit Registry state out of
  Git and into the Forseti Data Lake: append-only subreddit authority records
  that fold on read, a one-time baseline migration of the committed registry,
  the taxonomy-vocabulary-versus-row-assignment split, staged migration, and
  rollback. Mirrors the accepted Creator Registry Git-to-Lake cut-over at the
  lighter Creator Frontier tier.
use_when:
  - Deciding where live Reddit subreddit registry state lives.
  - Implementing or reviewing the Reddit registry lake cut-over.
  - Adding a tracked subreddit or radar observation without a data-only pull request, or checking the lake-authority-versus-Git-contract split.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/social_media/reddit/reddit_subreddit_registry_spec_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/reddit/reddit_radar_grid_capture_maintenance_design_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_lake_authority_contract_v1.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
stale_if:
  - The registry spec changes its row shape, two-speed rule, or feed contract.
  - The Creator Registry lake authority contract changes its authority/read-model split.
  - This cut-over is implemented and ratified (this proposal becomes the record or is superseded).
  - The radar grid design changes what a grid pass emits per subreddit.
```

## Status

`IMPLEMENTED — NOT RATIFIED`. The architecture below is unchanged from the
owner-accepted direction (2026-07-22) and has not been separately ratified;
what follows records only which stages executed.

| Stage | State | Evidence |
|---|---|---|
| 1 module, fold, CLI, gates | done | 44 unit tests; both lake touchpoint gates cleared |
| 2 baseline migration | done | 35 baselines, 106 observations, legacy sha256 `3e51ba47`, migration packet `01KY4FSZV3EB8GMJ305Z5KAWGB`, parity true / zero mismatches |
| 3a writer cut-over | done | 44 committed packets replay to zero writes, zero unknown |
| 3b live readback | done | packet `01KY4N5117KS4CB0EZNYJS3VAY`; fold advanced 4→5 observations, `status_observed_at` 2026-07-17→2026-07-22, `register_pointers` 2→3; re-run deduped to zero; committed JSON byte-unchanged |
| 4 move readers | satisfied by absence | no operational reader of the committed JSON remained: stage 3a moved the only consumer, and the fold is now its roster source |

Stage 4 required no edit. The surviving references to the committed file are the
migration input (`migrate` / `parity`) and the freeze guard that refuses to write
it — both of which this contract keeps. Removing the frozen file remains a later
work unit, unchanged.

A cross-vendor delegated code review returned four findings against the
implementation (RSR-01..RSR-04); all were verified against source, accepted, and
patched. This artifact asserts no validation, readiness, or ratification.

## Problem

`reddit_subreddit_registry_v0.json` is a Git-tracked 88K file holding live
operational state for 35 tracked subreddits. Every radar pass appends one
observation per subreddit, so every pass is a data-only pull request.

The evidence is concrete: the 2026-07-22 backfill, which copied already-committed
Bronze evidence into the registry and captured **zero new information**, produced
a `+435/-92` diff on a tracked file. At the accepted radar cadence (roughly
daily, 2–4x daily for trending subs) this becomes ~35 appended observations per
day, each one a commit against a tracked artifact.

This is the same pain the Creator Registry cut-over already resolved as doctrine:
live registry state is operational data and does not belong in Git.

## Precedent studied

The Creator Registry cut-over
(`creator_registry_lake_authority_contract_v1.md`, PRs #1254, #1263, #1272)
landed **two distinct tiers**, not one:

| Tier | Mechanism | Applied to |
|---|---|---|
| Heavy | Append-only authority in `derived/`, plus a generation-published read model under `indexes/derived_retrieval/creator_registry/` with a `CURRENT` pointer, content-derived generation ids, and fail-closed hash verification | Creator Registry — it feeds runtime preflight, monitoring eligibility, and a client-safe public profile |
| Light | Append-only records that fold on read; the contract states v1 has no `CURRENT` projection | Creator Frontier dispositions |

Observed lessons carried into this plan:

- The generation machinery is where the defects were. #1263 was a
  generation-cutover repair (collision, dry-run, CLI); #1272 hardened dry-run
  tests. The fold-on-read tier carried no equivalent repair.
- #1254 was routed through a different-vendor delegated review before landing.
- CI has no lake. All tests resolve through `DataLakeRoot.for_test`.
- Production migration is additive: old readers continue against Git until the
  new code lands, and the checked-in JSON stays frozen and non-authoritative for
  rollback until an independent live pass proves the lake route.

## Decision: Reddit uses the light tier

Reddit's registry has no client-safe projection, no cross-platform identity
resolution, no candidate-to-validated admission state machine, and no Judgment
binding. Its consumers are internal and operator-run: which subreddits get a
pass, per-subreddit baselines for the deferred breakout rule, and presence
checks from discovery and graph-frontier work.

Reddit therefore takes the **Creator Frontier shape**: append-only records that
fold on read, with no generation, no `CURRENT` pointer, and no generated
manifest. This deliberately skips the machinery that required two repair PRs in
the creator lane.

## Authority split

The cut is **taxonomy vocabulary versus row assignment**, not roster versus
observations.

Of the 18 fields on a registry row, the authored judgments are `niche_paths`,
`venue_roles`, `discovery_state`, and `source_pointers`. The stable `subreddit`
key is admitted identity, `url` is derived from it, and `status`,
`status_observed_at`, `created_utc_or_none`, `title_or_none`,
`public_description_or_none`, `posting_posture_or_none`,
`descriptive_observed_at`, `descriptive_changes`, `capture_state`,
`observations`, `register_pointers`, and `first_seen_at` are observed or
materialized facts. The row is predominantly lake-derived data that currently
happens to live in Git.

```text
Git retains (contract)          Lake holds (authority)
------------------------------  ----------------------------------------
niche_paths vocabulary          every subreddit row and its field values
venue_roles vocabulary          the dated observation series
the registry spec + this doc    roster membership and tag assignments
code, schemas, tests, fixtures  descriptive change records
frozen legacy JSON (rollback)   capture_state
```

The registry spec already establishes the vocabulary half as Git contract:
vocabularies are extended by adding a value in the spec first, then using it in
rows. That sentence survives the cut-over unchanged; only the rows move.

Roster additions become PR-free. This is load-bearing rather than incidental:
the Reddit graph frontier discovery arm
(`data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md`) exists
specifically to emit new candidate subreddits. While that arm is idle, roster
additions look rare; once it runs, they are continuous — the same condition that
moved Creator Frontier dispositions out of Git.

## Record shapes

```text
derived/<shard>/<subreddit>/reddit_subreddit_roster_change/<record-id>
derived/<shard>/<subreddit>/reddit_subreddit_observation/<record-id>
derived/<shard>/<subreddit>/reddit_subreddit_registry_baseline/<record-id>
```

`reddit_subreddit_registry_baseline_v1` — one-time, one record per subreddit,
carrying the normalized migrated legacy row and binding the exact legacy JSON
file hash plus its migration Source Capture packet. The packet preserves the
committed input bytes; the per-subreddit records are the foldable authority.

`reddit_subreddit_observation_v1` — append-only, one record per subreddit per
grid packet. Carries `observed_at`, `subscriber_count_or_none`,
`active_user_count_or_none`, `source_surface`, `provenance_pointer` (the Bronze
manifest), and `absent_reason_or_none`. The same record also carries the
grid-derived row effects the current materializer applies: the liveness
observation, monotonic `capture_state` upgrade, and `register_pointers` addition.
The fold therefore cannot append the observation while losing the associated
status, capture, or provenance update.

`reddit_subreddit_roster_change_v1` — append-only, for adding a tracked
subreddit and for changing non-grid row state: `niche_paths`, `venue_roles`,
`discovery_state`, descriptive fields and their observation dates/change
history, `source_pointers`, or a thread-driven `capture_state` upgrade. Assigned
vocabulary values must exist in the Git contract; an unknown value fails closed.
Each change names its predecessor head. Missing, divergent, or multiple heads
fail closed instead of letting filesystem order decide current state.

The fold requires exactly one baseline per known subreddit before accepting
delta records, verifies that all baselines bind the same legacy file hash, and
then applies roster changes by predecessor chain and observations by
`provenance_pointer`. A missing baseline, duplicate provenance pointer with
different bytes, identity mismatch, capture-state downgrade, or ambiguous
roster head fails closed. Whole-roster enumeration scans the subreddit anchor
directories; no derived-record availability index is implied by this v0.

### Anchor choice

Records anchor on the **subreddit name**, not the grid packet id.

`DataLakeRoot.append_record` writes to
`<subtree>/<anchor_shard>/<raw_anchor>/<lane>/<record_id>`, so the anchor
determines what is cheap to read. Reddit's dominant read is "give me this
subreddit's series" for baseline computation, which makes the subreddit the
right anchor — the account-anchored shape from the YouTube producer rather than
the packet-anchored shape from Instagram. The grid packet manifest remains
inside each record as `provenance_pointer`, so drill-back to Bronze is
preserved.

This applies the discovery lesson from the creator cut-over (AR-01 in
`creator_profile_current_lake_cutover_architecture_v0.md`): pick the anchor that
matches the read, because the anchor is part of the append-only record path and
changing it later is a data migration rather than a patch.

### Idempotence

Record ids are content-derived. Observation ids derive from the canonical
subreddit plus provenance pointer; roster-change ids derive from the canonical
change body including its predecessor. This preserves the current refresh
runner's rule that observations dedupe by provenance pointer, so re-feeding the
same packet is a no-op. An exact replay is `already_current`; a conflicting value
for the same content id fails closed.

## Migration stages

1. Add `forseti-harness/data_lake/reddit_subreddit_registry.py`: record schemas,
   content-derived ids, fail-closed fold, vocabulary validation, baseline
   migration, and a roster-change CLI surface (add or retag a subreddit).
   Temp-lake tests use `DataLakeRoot.for_test`; there is no production wiring.
   Regenerate `forseti-harness/data_lake/lake_touchpoint_inventory_v0.json` in
   this stage because the new lake writer trips
   `tests/contract/test_data_lake_inventory_gate.py`.
2. Preserve the exact committed JSON in a migration Source Capture packet, then
   dry-run and write the one-time baseline for all 35 rows, including the
   2026-07-22 backfill. Before the first authority write, prove the legacy file
   hash, subreddit set, per-subreddit observation counts, total observation
   count, and folded semantic parity. An identical rerun is `already_current`;
   differing baseline hashes or partial baseline sets are blockers. Existing
   readers and the refresh writer still use Git.
3. Repoint `run_reddit_subreddit_registry_refresh.py` to the lake writer while
   preserving `--dry-run`. Freeze the checked-in JSON bytes at this boundary;
   do not remove its rows. Run one independent live radar pass and prove the new
   observation plus its status/capture/provenance effects through the lake fold.
4. Move operational readers to the lake fold with no Git fallback only after
   the stage-3 readback passes. The frozen JSON remains a non-authoritative
   migration input and emergency stale snapshot; removing it is a later work
   unit, not part of this cut-over.

## Rollback

The checked-in registry JSON stays byte-frozen and non-authoritative for
rollback and audit through the first cut-over. Remove it only in a later work
unit after an independent live radar pass proves the lake route end to end.

Reverting means pausing registry-producing runs, stopping consumption of the
lake fold, and re-pointing readers at the frozen JSON. Lake records remain the
historical record and are replayed when the lake route resumes; nothing rewrites
them. This is a code-path rollback, not current-state parity: the fallback view
is stale from the stage-3 writer switch onward, and operators must surface that
freshness boundary rather than report the frozen view as current. Before an
external consumer binds, the schema route remains reversible; after one binds,
the versioned lake contract is sticky even if internal readers roll back.

## Accepted residuals and upgrade triggers

- **Fold-on-read and roster-enumeration cost grow with the series.** At daily
  cadence across 35 subreddits the series reaches roughly 12,700 records in a
  year, and a whole-roster read scans the subreddit anchor directories because
  `DataLakeRoot` has no derived-record availability index. The upgrade trigger
  to a generation-published index is a second consumer, duplicated discovery
  logic, or measured read latency — explicitly **not** record count alone,
  matching the Option 3 reasoning in the creator cut-over: records are read once
  to build an index, never rewritten, so deferring is cheap.
- **Roster edits lose pull-request review.** This is the point of the change,
  not a defect, but it shifts the burden onto fail-closed validation in the
  writer: unknown vocabulary values, identity conflicts, and duplicate roster
  additions must be refused rather than reviewed after the fact.
- **Subscriber counts remain absent on the public grid surface.** Old Reddit no
  longer renders the titlebox subscriber block on listing pages, so migrated and
  new observations carry an honest absent reason. This cut-over does not fix it;
  the subscriber series continues to depend on the `about.json` / sanctioned-API
  surface.
- **Stage 3 depends on separately authorized work.** The independent live radar
  pass that stage 3 requires as its readback is not authorized by this artifact:
  it needs its own capture authorization and a current source-policy/robots
  posture receipt per
  `reddit_radar_grid_capture_maintenance_design_v0.md`. Until that pass runs,
  stage 4 stays blocked and the frozen JSON remains the operational read.
- **Delegated review is not ratification.** The commissioned different-vendor
  review return remains decision input for Chief Architect adjudication; its
  working-tree diff and verdict do not change this artifact's `PROPOSAL` status.

## Non-claims

Not validation, readiness, implementation authorization, capture authorization,
live Reddit access, a lake write, ToS sufficiency, API registration, commercial
permission, scheduler or cadence authorization, breakout-rule design, demand
proof, or judgment evidence. Creates no database, event framework, scheduler, or
standing timing system.
