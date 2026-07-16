# Reddit Radar Grid-Capture Maintenance Design v0

```yaml
retrieval_header_version: 1
artifact_role: Design lane artifact (Reddit radar/registry maintenance pipeline; applies existing doctrine, changes none; designed-not-executed)
scope: >
  Owner-directed design for how the Reddit subreddit registry and thread-level
  radar are maintained: registry-filtered grid capture of subreddit
  best/top/rising pages into data-lake Bronze, breakout selection against
  registry baselines, deep-dive thread capture (TikTok-lane pattern), and a
  read-only registry materializer from committed Bronze. Records the owner's
  2026-07-16 cadence and dual-track access directions and names the gates
  still required before execution.
use_when:
  - Scoping or building the Reddit grid-capture runner, breakout rule, or registry materializer.
  - Checking the owner-directed cadence target and dual-track access posture for Reddit radar.
  - Checking what must be amended or re-verified before any cadenced Reddit capture executes.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/social_media/reddit/reddit_subreddit_registry_spec_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/reddit/README.md
  - forseti/product/spines/scanning/source_families/reddit/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_daily_heartbeat_operating_policy_v0.md
stale_if:
  - The Reddit source-access doctrine is amended (monitoring hard stop, robots/ToS posture, or commercial/API path) — then that amendment supersedes the gate list here.
  - A fresh Reddit policy re-check (robots.txt, Data API terms, Public Content Policy) changes what grid capture may touch.
  - The TikTok grid/deep-dive contracts this design mirrors change their packet or admission shape.
  - The registry spec changes its feed contract or observation shape.
```

## Status and non-claims

`DESIGN — DESIGNED_NOT_EXECUTED`. This is a maintenance **plan** applying
existing patterns (TikTok grid→deep-dive lane, creator-registry
materializer rule, bounded-run envelopes); it changes no doctrine and
authorizes no capture, no scheduler, no cadence, and no API registration.
Claims are `product_learning`-capped.

## Owner directions recorded (2026-07-16, in-thread)

1. **Cadence target: follow the TikTok lane pattern.** Roughly daily grid
   capture per tracked subreddit; trending/hot subreddits stepped up to
   2–4x daily. This is the design target, not an authorization — see the
   execution gates below.
2. **Access posture: dual-track, "we'll do both."** Public bounded capture
   AND a sanctioned Reddit API / licensing path are pursued together, not
   as either/or. Public capture carries the measured-risk ToS-gated
   posture; the sanctioned path covers cadenced/commercial-grade needs.
3. **The recorded Reddit policy check is stale.** The 2026-06-08 external
   posture check (robots.txt, Data API terms, Public Content Policy) in the
   graph-frontier architecture is ~1 month old per the owner; a fresh
   re-check is required at the execution gate, not assumed from that
   record.

## The maintenance pipeline

```text
registry filter (niche_paths/venue_roles)      e.g. beauty/fragrance, hub+dupe_value
        v
grid capture: one best/top/rising listing page per subreddit per pass
  - the one page carries BOTH layers: thread grid (titles, scores,
    comment counts) AND the sub envelope (subscribers, active-now, sidebar
    bio/rules)
  - packets -> data lake BRONZE (immutable, manifest-hashed, TikTok-style)
        v
breakout selection: thread engagement as an outlier vs THAT sub's own
registry baseline (subscriber series = the normalizer; a 500-comment
thread is breakout in a 39K sub, noise in a 2.4M sub)
        v
deep dive: selected threads through the existing exact-thread capture
route (old-Reddit direct HTTP) -> BRONZE
        v
registry refresh: a READ-ONLY materializer scans committed Bronze grid
packets (creator-registry rule: capture runners never flip registry state)
  - appends one observation per sub per pass (count, date, packet pointer)
  - diffs descriptive fields; appends a change record only on real change
  - flips capture_state when deep-dive packets exist
        v
thread-level derivations flow Bronze -> ECR/Silver source-agnostically as
today; subreddit-level Silver records are deferred until Judgment needs
them (each observation already carries its packet pointer, so promotion
later loses nothing)
```

Radar semantics: the radar payload is **thread-level** (which asks and dupe
waves are breaking out). The registry supplies routing (which subs get a
pass) and baseline (velocity denominator); it never stores a computed trend
or breakout claim.

## Execution gates (named, still closed)

1. **Monitoring hard stop.** The Reddit lane README currently hard-stops
   monitoring/production-crawler behavior. Cadenced daily/intraday grid
   capture is that class. Executing the cadence requires amending the
   owning source-access doctrine (DCP receipt, owner sign-off), which this
   design does not do.
2. **Fresh ToS/robots re-check** at build/execution time (direction 3
   above), recorded per bounded run as the existing envelopes require.
3. **Sanctioned API/licensing track** needs its own commercial decision and
   registration work before it exists; nothing here registers or commits to
   terms.
4. **Build items when commissioned:** grid-packet schema + capture runner
   (mirror TikTok grid contracts + old-Reddit HTTP route), the breakout
   rule (outlier definition over registry baselines), and the registry
   materializer runner. One-off bounded dry runs fit existing envelopes and
   are the right first probe before any cadence.

## Non-claims

Not validation, readiness, capture/scan/monitoring authorization, scheduler
authorization, API registration, commercial permission, ToS sufficiency,
doctrine amendment, demand proof, or judgment evidence.
