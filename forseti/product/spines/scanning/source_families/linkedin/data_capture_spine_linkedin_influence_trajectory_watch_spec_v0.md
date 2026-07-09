```yaml
retrieval_header_version: 1
artifact_role: Deferred-feature spec (non-authorizing, Bounded Watch capability)
scope: >
  How the LinkedIn Discovery & Planning Lane would track an actor's VISIBLE influence
  numbers over time (a coarse trajectory) to flag meteoric/rising public actors for
  watch prioritization. Deferred Bounded Watch capability; not slice 1 or slice 2.
use_when:
  - Designing the Bounded Watch stage's influence-trajectory tracking.
  - Deciding whether a small-but-fast-rising actor warrants watch / promotion consideration.
authority_boundary: retrieval_only
```

# LinkedIn Lane — Visible-Influence Trajectory Watch (deferred) v0

## What and why

Some worthwhile public actors are not big yet — they are *rising fast*
(meteoric / trending). To catch them without lowering the public-actor bar, the
lane would track the **trajectory of an actor's visible influence numbers over
time** and use a *rising* trajectory as a watch-prioritization signal.

This is **corroboration and prioritization, never a basis.** A concrete
public-actor basis is still required (architecture person-basis rule); a
trajectory only *strengthens* confidence or *flags* a smaller actor as worth
watching. It is explicitly **not** the social graph — relationship-graph capture
stays forbidden (see Hard Stops and `data_capture_spine_future_exploration_lanes_v0.md`).

## What is tracked — and only this

Point-in-time snapshots of the **visible counts / coarse bands the lane already
allows**:

- `follower_count_or_none`, `connection_count_band_or_none`,
  `subscriber_count_or_none`, `engagement_count_or_none`;
- each with an observation `timestamp` and the `source_surface` it was visible on.

The **trajectory** is the ordered series of these snapshots (a velocity / growth
signal). Nothing else: no follower / connection / commenter *list or graph*, no
profile body, no post content, no contact fields.

## Boundaries (inherited from Bounded Watch + Hard Stops)

- A few **coarse** snapshots within a declared watch window — **not a full
  timeline** (the architecture's Bounded Watch forbids full timelines and
  indefinite life-tracking).
- Declared **watch window + stop date + caps**; stop on window-elapsed / caps /
  privacy drift.
- **Visible counts/bands only**; minimization unchanged; every row stays
  **planning-only**.
- The social graph stays forbidden; trajectory ≠ graph.
- Storage is a **local, operator-held planning artifact** — not a durable people
  dataset, datastore, scheduler, or dashboard.
- One snapshot = one observed visible number at a point in time; snapshots are
  not merged into a derived profile.

## Selection use

A rising trajectory may flag a **smaller** actor (below absolute-count
expectations) as worth watching or considering — but **promotion still requires
the separate promotion gate and a concrete public-actor basis.** Trajectory never
auto-promotes and never substitutes for the basis.

## Where it lives / status

A **deferred Bounded Watch (stage 2) capability** — *not* slice 1 (discovery
rows) or slice 2 (frontier register). It would be built under its own scoping
when Bounded Watch is taken up.

## Open design questions (for build time)

- snapshot cadence and how many snapshots are retained (favor few + coarse for
  minimization);
- exact count vs coarse-band granularity;
- how "rising / meteoric" is computed (delta, rate, threshold) without
  over-collecting;
- the artifact shape for the snapshot series (local planning artifact only).

## Non-claims

Deferred and **not authorized**; not a current build spec; **not** the social
graph; not content/contact capture; not a durable people dataset; not validation
or readiness. A forward-looking design for a Bounded Watch capability only.
