# Reddit Radar Grid-Capture Maintenance Design v0

```yaml
retrieval_header_version: 1
artifact_role: Design lane artifact (accepted Reddit radar/registry maintenance pipeline; designed-not-executed)
scope: >
  Accepted design for how the Reddit subreddit registry and thread-level
  radar are maintained: registry-filtered grid capture of subreddit
  best/top/rising pages into data-lake Bronze at the accepted cadence
  (roughly daily; 2-4x daily for trending subs), breakout selection against
  registry baselines, deep-dive thread capture (TikTok-lane pattern), a
  read-only registry materializer from committed Bronze, and the dual-track
  access posture (bounded public capture AND a sanctioned API/licensing
  path in parallel).
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
  - The Reddit lane README amends the radar cadence, hard stops, or dual-track access posture again.
  - A fresh Reddit policy re-check (robots.txt, Data API terms, Public Content Policy) changes what grid capture may touch.
  - The TikTok grid/deep-dive contracts this design mirrors change their packet or admission shape.
  - The registry spec changes its feed contract or observation shape.
```

## Status and non-claims

`DESIGN_ACCEPTED — DESIGNED_NOT_EXECUTED` (owner, 2026-07-16). The cadence
and access posture below are the current doctrine, carried by the Reddit
lane README; this artifact is their design record. Nothing is built or
running: no runner, no scheduler, no API registration exists yet, and
claims are `product_learning`-capped.

## Accepted design parameters

1. **Cadence: TikTok lane pattern.** Roughly daily grid capture per
   tracked subreddit; trending/hot subreddits stepped up to 2–4x daily.
2. **Access: dual-track.** Bounded public capture under the measured-risk
   ToS-gated posture AND a sanctioned Reddit API / licensing path,
   pursued in parallel; commercial-grade product use lands on the
   sanctioned path.
3. **Policy currency.** The 2026-06-08 external posture check (robots.txt,
   Data API terms, Public Content Policy) is superseded as a currency
   basis; each run records its own fresh robots/source-policy posture
   receipt, and the build gate re-checks the three policy surfaces.

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

## Storage and retention

Keep-all-raw does not survive scale: measured grids are ~96% CSS/JS/chrome,
while the canonical rows retain the source-visible venue and post facts.
Current fleet and deep-dive capture therefore uses the same two-state rule as
other rendered sources:

1. **Content is the admitted default.** Acquisition extracts the canonical
   content record before publication, hashes the disposable HTML/text inputs,
   and discards them only after successful extraction.
2. **Raw is explicit compatibility evidence.** It is retained only when a
   commissioned investigation genuinely needs the original transport body.
   Historical raw packets remain immutable and readable through the contained
   legacy decoder.
3. **Qualification is scratch, not a third packet mode.** A bounded operator
   run may compare fresh raw inputs with fresh deterministic extraction before
   admission. Match deletes only those scratch DOM/text inputs; drift preserves
   them with a report. No sample packet enters the lake.
4. **Provenance is never dropped.** URL, capture timestamp, HTTP/source-policy
   receipt, hashes and byte counts of discarded inputs, extractor version, and
   the canonical content-record hash remain packet evidence.

The named loss is replay under a future extractor. On-demand live recapture is
the honest mitigation; Forseti does not pay an indefinite fleet-wide raw or
sample retention tax merely to preserve that option. Cleaning validates and
adapts current content records directly. There is no Reddit post-hoc capture
Projection lane.

## Remaining gates before execution

1. **Fresh policy re-check at build time** (robots.txt, Data API terms,
   Public Content Policy), plus the per-run robots/source-policy posture
   receipt every pass already owes.

   **Evaluate a re-check against the decision predicate, not the prior
   description.** The predicate is: *the captured listing surface is
   robots-disallowed for us, and the owner accepted capturing it anyway as a
   bounded pass.* Halt and return to the owner only when that could change — the
   surface becomes allowed (the measured-risk posture is then moot and must be
   re-derived), a hard access gate appears, the accepted bound or cadence is
   exceeded, or use becomes commercial-grade. Otherwise proceed and record: a
   broader or reworded disallow leaves the predicate true.

   This exists because the 2026-07-22 re-check halted an authorized pass on a
   change that could not flip the decision. The receipt recorded a *description*
   of the file, which reads as a scope claim, so a broader reality looked like a
   change rather than a confirmation.

   **Re-check executed 2026-07-22 — recorded; NOT a blocker.**
   `https://www.reddit.com/robots.txt` and `https://old.reddit.com/robots.txt`
   both now serve exactly:

   ```text
   User-agent: *
   Disallow: /
   ```

   Verified across three probes (generic agent string, plain browser string,
   and no `User-Agent` header) on both hosts; the response is
   user-agent-independent and the file cites Reddit's Public Content Policy as
   the governing access restriction. This is a **blanket** disallow for every
   generic agent, not the granular per-surface disallow list recorded on
   2026-06-08, and it is broader than the standing per-run receipt in
   `run_reddit_grid_capture.py`, which states only that "robots.txt disallows
   subreddit listing surfaces for generic agents" — still true, now materially
   understated.

   **Diagnosed, not assumed.** Three alternative explanations were tested and
   all fail:

   - *Intermittent?* No. Five consecutive fetches returned the identical
     538-byte body.
   - *Our egress being served a punitive file?* No. The egress is residential
     (AS9506 Singtel, SG) with no proxy, and the Internet Archive's independent
     crawl of `reddit.com/robots.txt` on 2026-04-14 is **byte-identical** to
     what we receive.
   - *A recent change we could wait out?* No. Across 2026 the archive shows
     Reddit alternating between exactly two variants — `User-agent: * /
     Disallow: /` (what we get) and `User-Agent: * / Allow: /$ / Disallow: /`.
     The second permits only the bare homepage. **Neither variant permits a
     subreddit listing path.**

   **Why this is not a blocker.** The change is one of degree, not kind. The
   accepted posture already states that the captured surface is
   robots-disallowed — the per-run receipt in `run_reddit_grid_capture.py` reads
   "robots.txt disallows subreddit listing surfaces for generic agents; this
   bounded single-page grid pass runs under the owner-accepted measured-risk
   dual-track posture." A subreddit listing path is disallowed under the granular
   file and under both current variants alike, so nothing decision-relevant to
   this lane moved. The receipt's operative clause stands; only its implied
   picture of the surrounding file is stale.

   robots.txt is also advisory, not enforcement: Reddit serves listing pages
   normally, and the lane's captures have continued to succeed (most recent
   Reddit packet 2026-07-18). Capture success is not evidence of robots
   permission, and robots disallow is not evidence of a broken capture path —
   the two measure different things, and the measured-risk posture exists
   precisely because they diverge.

   **Accuracy correction for the prior record:** the granular per-surface list
   was last served in 2025, so the 2026-06-08 observation carried by
   `data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md` described
   a file already withdrawn. Its operative clause — subreddit listings
   disallowed — was correct then and remains correct. The correction is to the
   description, not to the accepted risk basis.

   The standing per-run receipt should be reworded to state the blanket
   disallow accurately rather than implying a granular file, but the posture it
   records is unchanged and no re-authorization is required for it.
2. **Sanctioned API/licensing track** needs its own registration and
   commercial-terms work before it exists; nothing here registers or
   commits to terms.
3. **Build state (2026-07-17):** the grid capture runner
   (`forseti-harness/runners/run_reddit_grid_capture.py`,
   `source_family="reddit_subreddit_grid"`), the lake-committing deep-dive
   route (`run_reddit_old_http_batch.py --data-root`), and the registry
   materializer (`run_reddit_subreddit_registry_refresh.py`) exist and were
   exercised live against r/MakeupAddiction (grid packet + top-thread
   deep-dive committed to Bronze; registry refreshed from the packet).
   Still open: the breakout rule (owner-deferred until enough passes
   accumulate per-sub behavior distributions; radar pass 001 on 2026-07-17
   is observation #1), and venue subscriber counts on the public grid
   surface — old Reddit no longer renders the titlebox subscriber block on
   listing pages, so grid observations carry an honest absent reason and
   the subscriber series continues via the `about.json`/sanctioned-API
   surface (the API adapter needs a small `about` mode once credentials
   exist).

   **Subscriber absence diagnosed 2026-07-22 (bounded qualification run, raw
   retained to scratch, nothing admitted).** The extractor is correct, not
   stale. In 284 KB of served old-Reddit listing HTML the `titlebox` element is
   present but its volume block is gone: zero occurrences of `subscribers`,
   `users-online`, `readers`, or `span class="number"`. The count is not hidden
   elsewhere either — no `"subscribers": N` JSON field, no `accounts_active`,
   and **no comma-formatted six-digit number anywhere on the page.** The
   titlebox now holds the subreddit name, the join/leave toggle, and the sidebar
   text, with the reader and users-here-now lines removed outright.

   One variable remains untested: the payload reports `"logged": false`, so
   whether an authenticated old-Reddit render still carries the block is
   unknown. That is the cheapest next probe (there is already a
   `run_source_capture_reddit_credential_bootstrap.py`), and it would decide
   between "removed for everyone" and "removed for logged-out views". Either way
   `about.json` remains the working path — the 2026-07-16 observations that do
   carry counts came from exactly that surface.

   **Enumeration note.** `indexes/derived_retrieval/bronze_catalog` is a
   rebuildable derived projection and lags until rebuilt; it did not list the
   2026-07-22 packet that `DataLakeRoot.list_available` did. Enumerate committed
   packets from `list_available`, not the catalog. Enumerating from a lagging
   index is the same failure family as the 2026-07-22 backfill gap, where 35
   subreddits had committed packets but only 7 were recorded.

## Direction Change Propagation

```yaml
# storage-and-retention direction 2026-07-17 (owner).
direction_change_propagation:
  doctrine_changed: >
    Reddit radar storage uses canonical content by default, explicit raw only
    when commissioned, and scratch-only qualification rather than admitted
    sample packets. Acquisition retains provenance and hashes discarded inputs;
    Cleaning owns validation/adaptation, historical raw remains immutable and
    readable, and no post-hoc capture Projection lane remains.
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - forseti/product/spines/capture/core/source_families/social_media/reddit/reddit_radar_grid_capture_maintenance_design_v0.md
  downstream_surfaces_checked:
    - forseti/product/spines/capture/core/source_families/social_media/reddit/README.md
    - forseti/product/spines/capture/core/source_families/social_media/reddit/reddit_subreddit_registry_spec_v0.md
    - forseti-harness/runners/run_reddit_grid_capture.py
    - forseti-harness/capture_spine/reddit_subreddit_grid/materializer.py
  intentionally_not_updated:
    - path: forseti/product/spines/capture/core/source_families/social_media/reddit/README.md
      reason: >
        The README's radar section already routes to this design for
        pipeline mechanics; retention is design-level detail and a second
        statement would fork the owner.
    - path: forseti-harness/runners/run_reddit_grid_capture.py
      reason: >
        Current keep-raw behavior stands until the content-packet writer
        build gate; no code change is authorized by this direction alone.
    - path: forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
      reason: >
        The repo-wide content-mode-standard posture lands in the playbook
        in the same work unit that builds the family-agnostic writer seam
        (Phase A); recording it there before the capture mode exists would
        instruct operators toward a route that does not run yet.
  stale_language_search: >
    rg -n -i "keep raw|keep-all|retention|content packet|raw sample"
    forseti/product/spines/capture/core/source_families/social_media/reddit
  stale_language_search_result: >
    Executed 2026-07-17 after the edit. Hits are this new section and
    receipt; no other live Reddit-lane surface states a keep-all-raw or
    conflicting retention rule.
  non_claims:
    - not validation or readiness
    - not implementation of the content-packet writer
    - not retroactive deletion authorization
    - not ToS sufficiency
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    The Reddit capture lane's blanket monitoring/scheduler/cadence hard stop
    and single-track commercial posture are replaced: registry-scoped radar
    grid capture at roughly daily cadence (2-4x daily for trending subs,
    TikTok-lane pattern) is an accepted direction, and access is dual-track
    (bounded public capture under the measured-risk ToS-gated posture AND a
    sanctioned commercial/enterprise API or licensing path in parallel,
    with commercial-grade product use landing on the sanctioned path).
    Broad crawling beyond registry-tracked grid passes, user/profile
    capture, and dashboards remain hard-stopped; the 2026-06-08 policy
    check is superseded as a currency basis by build-time and per-run
    posture receipts.
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - forseti/product/spines/capture/core/source_families/social_media/reddit/README.md
    - forseti/product/spines/capture/core/source_families/social_media/reddit/reddit_radar_grid_capture_maintenance_design_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/reddit/reddit_subreddit_registry_spec_v0.md
  downstream_surfaces_checked:
    - forseti/product/spines/scanning/source_families/reddit/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md
    - forseti/product/spines/scanning/source_families/reddit/reddit_beauty_fragrance_subreddit_inventory_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/reddit/reddit_subreddit_registry_v0.json
    - forseti/product/spines/scanning/README.md
  intentionally_not_updated:
    - path: forseti/product/spines/scanning/source_families/reddit/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md
      reason: >
        Its 2026-06-08 policy observations are a dated point-in-time receipt,
        not a live rule; its stale_if already fires on source-access posture
        change, and the frontier lane's own boundaries (no same-run
        traversal, bounded hops) are untouched by the radar cadence.
    - path: forseti/product/spines/capture/core/source_families/social_media/reddit/reddit_subreddit_registry_v0.json
      reason: >
        Registry non-claims ("not a crawl queue or standing monitor") remain
        true: the radar lane does the cadenced capture; the registry stays a
        derived state projection.
  stale_language_search: >
    rg -n -i "monitoring|scheduler|standing monitor|sanctioned|hard stop"
    forseti/product/spines/capture/core/source_families/social_media/reddit
    forseti/product/spines/scanning/source_families/reddit
  stale_language_search_result: >
    Executed 2026-07-16 after the amendment. Remaining hits are the new
    cadence/dual-track text itself, still-true artifact non-claims (the
    registry, inventory, and README each still authorize no monitoring
    themselves), and the graph-frontier lane's own untouched
    no-scheduler-in-this-lane boundaries. No live rule contradicting the
    accepted radar cadence or dual-track posture remains.
  non_claims:
    - not validation or readiness
    - not capture execution authorization for an unbuilt lane
    - not ToS sufficiency or legal advice
    - not API registration or commercial terms
    - not demand proof or judgment evidence
```

## Non-claims

Not validation, readiness, execution authorization for the unbuilt lane,
scheduler existence, API registration, commercial permission, ToS
sufficiency, demand proof, or judgment evidence.
