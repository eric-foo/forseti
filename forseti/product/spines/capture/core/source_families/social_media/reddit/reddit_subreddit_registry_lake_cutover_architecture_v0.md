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
  - Adding a tracked subreddit or a radar observation without a data-only pull request.
  - Checking which registry content is lake authority versus Git contract.
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

`PROPOSAL` — pre-ratification, planning only. Owner accepted the direction to
move the registry out of Git (2026-07-22) and chose the plan-artifact-first
route. Nothing here authorizes implementation, capture, live Reddit access, or
a lake write. No code has been written against this proposal.

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

Of the 18 fields on a registry row, only `niche_paths`, `venue_roles`, and
`discovery_state` are hand-assigned. `status`, `status_observed_at`,
`created_utc_or_none`, `title_or_none`, `public_description_or_none`,
`posting_posture_or_none`, `descriptive_observed_at`, `descriptive_changes`,
`capture_state`, `observations`, `register_pointers`, and `first_seen_at` are
observed or materialized facts. The row is predominantly lake-derived data that
currently happens to live in Git.

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
carrying the migrated legacy row exactly as committed.

`reddit_subreddit_observation_v1` — append-only, one record per subreddit per
grid packet. Carries `observed_at`, `subscriber_count_or_none`,
`active_user_count_or_none`, `source_surface`, `provenance_pointer` (the Bronze
manifest), and `absent_reason_or_none`, matching today's observation shape so
the migration is a re-home rather than a reshape.

`reddit_subreddit_roster_change_v1` — append-only, for adding a tracked
subreddit and for changing `niche_paths`, `venue_roles`, `discovery_state`, or
descriptive fields. Assigned values must exist in the Git vocabulary; an unknown
value fails closed.

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

Record ids are content-derived. Observation ids derive from the provenance
pointer, preserving the property the current refresh runner already has: the
spec's re-run rule is that observations dedupe by provenance pointer, so
re-feeding the same packet is a no-op. An exact replay is `already_current`; a
conflicting value for the same content id fails closed.

## Migration stages

1. `forseti-harness/data_lake/reddit_subreddit_registry.py` — record schemas,
   content-derived ids, fold-on-read loader, vocabulary validation. Temp-lake
   tests via `DataLakeRoot.for_test`. No production wiring.
2. Repoint `run_reddit_subreddit_registry_refresh.py` to append observations to
   the lake, preserving `--dry-run`. Both read paths remain available.
3. One-time baseline migration of all 35 committed rows, including the
   2026-07-22 backfill. A dry run must prove the subreddit set and observation
   counts before the first authority write. Identical rerun is `already_current`;
   differing baseline hashes are a blocker.
4. Retire the committed rows from the tracked JSON, leaving vocabulary and
   doctrine. Operational readers move to the lake fold and do not fall back to
   Git.
5. Regenerate `forseti-harness/data_lake/lake_touchpoint_inventory_v0.json`.
   A new lake writer trips `tests/contract/test_data_lake_inventory_gate.py`,
   so this is a required step, not cleanup.

A roster-change CLI surface (add a subreddit, retag one) belongs with stage 2 or
later; it is the reviewed front door that replaces pull-request review of roster
edits, mirroring `run_creator_registry_lake.py`.

## Rollback

The checked-in registry JSON stays frozen and non-authoritative for rollback and
audit through the first cut-over. Remove it only in a later work unit, after an
independent live radar pass proves the lake route end to end.

Reverting means stopping consumption of the lake fold and re-pointing readers at
the frozen JSON. Lake records may remain as historical artifacts; nothing
rewrites them. The revert is clean while no external consumer has bound to the
lake read path.

## Accepted residuals and upgrade triggers

- **Fold-on-read cost grows with the series.** At daily cadence across 35
  subreddits the series reaches roughly 12,700 records in a year. The upgrade
  trigger to a generation-published index is a second consumer or measured read
  latency — explicitly **not** record count alone, matching the Option 3
  reasoning in the creator cut-over: records are read once to build an index,
  never rewritten, so deferring is cheap.
- **Roster edits lose pull-request review.** This is the point of the change,
  not a defect, but it shifts the burden onto fail-closed validation in the
  writer: unknown vocabulary values, identity conflicts, and duplicate roster
  additions must be refused rather than reviewed after the fact.
- **Subscriber counts remain absent on the public grid surface.** Old Reddit no
  longer renders the titlebox subscriber block on listing pages, so migrated and
  new observations carry an honest absent reason. This cut-over does not fix it;
  the subscriber series continues to depend on the `about.json` / sanctioned-API
  surface.
- **This proposal is not adversarially reviewed.** The creator equivalent was
  routed through different-vendor delegated review before landing.

## Non-claims

Not validation, readiness, implementation authorization, capture authorization,
live Reddit access, a lake write, ToS sufficiency, API registration, commercial
permission, scheduler or cadence authorization, breakout-rule design, demand
proof, or judgment evidence. Creates no database, event framework, scheduler, or
standing timing system.
