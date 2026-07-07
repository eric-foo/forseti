# Aphrodite Creator Capture Strategy v0

```yaml
retrieval_header_version: 1
artifact_role: Research strategy record (Aphrodite creator capture posture; not capture authorization)
scope: >
  Source-backed strategy for Aphrodite Signals creator capture before roster-size
  calculation: onboarding fingerprint, registry grid heartbeat, selective deep
  capture, stale-content handling, and the boundaries between Capture/Silver,
  Creator Signal, and any later activation arm.
use_when:
  - Deciding whether Aphrodite should prioritize daily grid refresh, deep reel/video capture, or both.
  - Preparing the later roster-size and request-budget calculation.
  - Checking how fragrance depth can compound without turning Aphrodite into manual agency work.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/creator_signal/creator_signal_product_architecture_v0.md
  - forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/README.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_index_spec_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_ledger_operational_evolution_contract_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_metric_silver_record_contract_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_record_contract_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/instagram/forseti_creator_monitoring_policy_architecture_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_at_scale_operating_envelope_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_profile_grid_dom_engagement_recon_and_spec_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_spec_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
source_context_notes:
  - Current origin/main in this worktree uses the renamed `forseti/` product root.
  - The creator_registry/profile-current contracts are present under the Forseti path and are treated as current source context for this strategy.
  - Root-local Aphrodite D-1 v1 rehearsal files observed in the dirty main workspace were not used as ratified current-main authority.
stale_if:
  - Creator registry/profile-current contracts move again or change metric, freshness, or identity boundaries.
  - IG monitoring policy changes the serious-v0 roster gates, A/B/C allocation, hot-list promotion, or capture-once/recheck posture.
  - A later accepted Aphrodite product contract supersedes this capture strategy.
  - Platform access constraints or measured request costs change materially.
```

## Status

`PROPOSED_RESEARCH_STRATEGY_V0`.

This is a strategy record, not implementation authority, capture authorization,
bot-detection guidance, live monitoring approval, data-lake write approval,
buyer proof, product readiness, or a final roster-size calculation.

## Core Strategy

Aphrodite should use a two-layer capture posture:

```text
daily grid heartbeat -> selective deep capture -> source-backed Creator Signal projection
```

The grid heartbeat is the cheap, broad, current layer. It answers: what changed,
which posts are moving, what entered the visible current surface, and what
deserves attention now.

Deep capture is the earned depth layer. It answers: why did this specific piece
work, what did it sell, which product/category/brand claims are source-backed,
what did comments/transcripts/captions show, and what limitations travel with
the evidence.

Do not deep-capture every video for every registry creator every day. That is the
budget trap. The correct compounding move is daily grid refresh for the registry,
then promote only the posts that earn deeper treatment.

## Why This Fits The Source Contracts

Creator Signal's ratified direction is foundation-first: build the live,
longitudinal, vertical evidence graph before overcommitting to a customer product.
Fragrance is the wedge and beauty/skincare is the destination. The strategy here
serves that by starting the time-series clock without prematurely freezing a
buyer-facing claim schema.

The IG monitoring policy already separates low-cost monitoring from hot-list
promotion. It warns that full curves on everything are the budget trap, and it
uses momentum as an allocator. This strategy makes that allocator explicit for
Aphrodite: grid first, deep only when the post becomes decision-useful.

The IG grid spec says grid capture is the primary v0 source for views, likes, and
comment counts. Per-reel capture is detail evidence for captions, transcripts,
audio/detail, and comments. Therefore deep capture can enrich the signal, but it
must not silently replace the grid-primary metric snapshot unless a later
selection-policy version says so.

The Silver Vault contract keeps raw truth, derived observations, and generated
read models separate. Missing, hidden, blocked, not-attempted, and not-applicable
facts must carry posture and reason, never fake zeroes. Aphrodite's selection
logic must inherit that rule.

The Creator Ledger operational contract makes exact known-account lookup and
scan/capture preflight the first routing layer. Aphrodite should not start by
treating a handle as new and then checking the registry later; that reverses the
ledger's main operational value.

## Onboarding Flow

For a new creator:

1. Run the Creator Registry exact-match/preflight check first. If the public
   platform account is already known, attach the observation and future capture
   work to the existing account row. If it is a possible match, route it as a
   candidate review item. Only truly unknown accounts should proceed as new
   candidate stubs.
2. Capture the current grid surface, with bounded pagination only if the run
   budget and capture policy allow it.
3. Build an onboarding fingerprint from source-visible metrics: views,
   likes/comments where available, engagement rate where numerator and
   denominator are observed, sample support, freshness, and source limitations.
4. Select the top diagnostic slice of visible content for deep capture. The
   target slice is roughly the top 20-25 percent of eligible current-grid items,
   selected by views plus engagement, not raw views alone.
5. Deep-capture that selected slice for detail evidence: transcript/caption,
   comments when available, product/category/brand mentions, disclosure fields
   only when source-exposed, and content-format clues. Store these as evidence
   with source pointers, not as unstamped conclusions.
6. Admit the creator into the registry/roster only with the allowed public
   account fields, operational tier/state, sub-niche label or pointer, source
   evidence, limitations, and freshness posture.

The onboarding fingerprint is an admitted-pool view, not a channel-wide creator
average. It should say what it covered and what it did not cover.

## Registry Monitoring Flow

For a registry creator:

1. Run the daily grid heartbeat as the default refresh.
2. Compare the current grid to the prior known snapshot: new content, retained
   content, metric deltas, newly eligible items, and items falling out of the
   visible grid.
3. Update Silver/Creator Registry metric records from the heartbeat before the
   product surface uses the snapshot. Grid heartbeat is not just UI refresh; it
   is the source-backed metric observation and rollup feed.
4. Promote a post to deep capture only when an event trigger fires: an unusual
   view or engagement delta, a fresh breakout state, a source-visible buyer-
   relevant cue, or a previously promoted breakout that is still inside its
   explicit recheck window.
5. Keep the high-alert watch list dynamic. It should be post-led and metric-led,
   not a static vanity list of favorite creators.
6. Recheck promoted breakout posts while they remain active, then demote them
   when their growth decays or their evidence has been captured sufficiently.

The daily heartbeat is the registry's currentness layer. The deep queue is the
explanation layer. They should be budgeted separately.

## Promotion Rule

The phrase "top 20-25 percent" should mean two different things in two
different contexts:

- **Onboarding:** a first-pass deep-capture budget cap over the visible current
  grid. It is a diagnostic sample, not a claim that the selected posts are the
  creator's durable best work.
- **Ongoing monitoring:** not the primary trigger. Ongoing deep capture should
  be event-triggered, with the top-band calculation used only as a supporting
  clue or capacity cap.

This prevents a bad local baseline from wasting budget. A weak creator can
always have a "top 25 percent" of their own posts; that does not mean those posts
deserve deep capture.

The promotion key should be composite and posture-aware:

```text
candidate_promotion_signal =
  observed view_count
  + observed like/comment counts where exposed
  + engagement_rate only when numerator and denominator are observed
  + delta since prior grid heartbeat where the prior observation exists
  + age/window normalization only when publication timing is source-backed
  + source-visible buyer-relevant cue when available
```

Use the gates this way:

- `spike_gate`: observed metric delta is unusually high against the creator's
  compatible recent baseline or the platform/content-kind norm. This can promote
  a post into first deep capture.
- `fresh_breakout_gate`: a new or recent item is both high-performing and still
  growing, not merely high in lifetime views. This can promote a post into first
  deep capture.
- `buyer_relevance_signal`: source-visible text or metadata indicates fragrance,
  product, category, ad, or comparison relevance. In v0 this is a prioritization
  and interpretation label, not a hard pre-capture gate.
- `active_breakout_gate`: a previously promoted item still has enough measured
  slope to justify follow-up metric recheck. It should not trigger repeat deep
  capture by default.

The v0 entry rule is:

```text
deep_capture_entry =
  (spike_gate OR fresh_breakout_gate)
  AND capture_budget_available
  AND post_not_already_deep_captured
```

Buyer relevance is assigned as an evidence label after capture, or as a weak
pre-label when source-visible caption/title/description/product/ad metadata is
already available. Do not require buyer relevance before deep capture. A
creator's top non-fragrance or non-buyer post can still be decision-useful: it
shows the creator's winning format, hook, audience response, and possible Studio
or brand-insertion surface.

After capture, classify the post as one of:

- `fragrance_buyer_relevant`;
- `fragrance_adjacent`;
- `non_fragrance_winning_format`;
- `commercial_adaptable_format`;
- `irrelevant_to_aphrodite`.

Do not offer `recent_velocity` as an observed field until compatible history
exists. If publication timestamp is missing or unreliable, call the trend
`capture-window delta`, not posting cadence or content age velocity.

Nulls and unavailable metrics are not zeros. A post with hidden or missing inputs
can still be retained for qualitative review, but it must not be ranked as if the
missing value were poor performance.

## Falling Out Of Grid

The default rule is:

```text
falls out of visible grid -> cold by default
```

That matches short-form reality: if a reel/short no longer appears in the
current grid and was never promoted, it usually no longer carries live momentum
worth spending daily capture budget on.

But the rule cannot be absolute. The exception is:

```text
previously promoted breakout/durable-watch item -> keep explicit recheck state until expiry
```

Otherwise Aphrodite would delete the rare long-tail exceptions that teach the
system what durable creator demand looks like. The exception must be explicit,
source-backed, and self-expiring. No hidden forever-watch list.

For promoted breakout items that fall out of grid view, use one or two explicit
known-item metric rechecks so the item can be retired cleanly. Prefer the
cheapest direct locator path already captured for that item. Do not use breakout
follow-up as a general pagination or old-content crawler. Stop rechecking when
growth slope falls below the accepted threshold for the accepted number of
checks, when an age cap or read cap is hit, or when the source blocks the path.

## Roster Composition Before Sizing

Do not make the whole roster pure fragrance reviewers if the product goal is
creator decision intelligence for fragrance brands. Pure reviewers are the core,
but Aphrodite also needs controlled adjacent surfaces:

- fragrance-native reviewers and collectors;
- fragrance-heavy lifestyle, GRWM, grooming, beauty, and menswear creators;
- creators with source-backed prior fragrance ads or repeated fragrance content;
- a small control/edge set that looks attractive by surface metrics but may not
  move fragrance.

The control/edge set is not the bottom 10 percent of the registry. Bottom
performers mostly teach that weak accounts are weak. The useful control set is
surface-attractive but fragrance-weak: creators with strong-looking reach or
engagement whose source-backed fragrance relevance is unproven, thin, or
negative.

Keep the control/edge set in the registry, but default it to low-cadence
monitoring or bounded test windows, not daily deep monitoring. Promote a control
creator into normal monitoring only if source-backed fragrance relevance or
fragrance-specific response appears. Otherwise it stays as false-positive
training data and cost control.

Exact percentages are deferred until the capture budget is calculated. The
strategic constraint is that adjacent creators must be fragrance-proven or
explicitly labeled as controls. Do not branch into broad GRWM/lifestyle just
because it is adjacent to beauty.

## Data-Layer Placement

Use the layers this way:

- Raw capture/lake: source material, packet ids, hashes, manifests, access and
  availability facts.
- Silver: source-backed observations, relationships, text observations, metric
  observations, metric rollups, posture/value coupling, and lineage.
- Creator registry/profile-current: current public account profile, latest
  allowed rollups, source drill-back, freshness, limitations, and identity
  boundaries.
- Aphrodite Signals: buyer-facing or operator-facing decision surface over
  stamped fields and visible limitations.
- Aphrodite Studio/Activation: optional downstream service consumer after
  Signals can identify the decision. It must not become the data authority.

Silver can say what was observed. Creator Signal can assemble decision support.
Gold/Judgment or later accepted product contracts own stronger recommendations,
durability verdicts, or action meaning.

## Visual And Metadata Boundary

Do not assume the daily grid heartbeat includes thumbnail or picture
understanding. Current platform surfaces differ:

- IG Reels grid capture can preserve locators, timestamps when joined, metric
  observations, passive JSON metadata, and caption text when the passive JSON
  join exposes it. The current IG grid runner has a route-specific option that
  defaults to blocking image/media/font requests to reduce bandwidth; that is an
  implementation posture, not a universal product rule.
- YouTube RSS monitoring exposes title, published/updated time, views, and the
  feed's star-rating count used as like-count provenance. It does not expose
  comment count in the current feed schema.
- YouTube watch-page packets can expose richer metadata and comment surfaces,
  but that is a deeper read than the cheap RSS heartbeat.
- TikTok is deferred for Aphrodite's immediate posture, but its recorded spec
  says item blobs can expose description, hashtags/mentions, play/like/comment
  counts, share/collect counts, and source-native subtitle metadata when present.

Visual/OCR or thumbnail interpretation is a separate optional evidence lane. It
may be valuable for posts where text metadata is thin, but it should be measured
as its own capture mode: normal asset loading may look more human and may reduce
some fingerprint oddities, while also increasing bandwidth, page weight, storage,
processing, and exposure to route-specific platform behavior. Do not claim that
blocking assets or loading assets is categorically safer; measure the route.

## Silver And Registry Metric Update Rule

Every accepted heartbeat should update the ongoing metric layer before Aphrodite
Signals relies on it. The current Creator Profile contract already exposes
average views, median views, average like count, average comment count,
engagement rate, posting cadence, and recent velocity fields, while
`posting_cadence` and `recent_velocity` remain declared-deferred until compatible
Silver history exists.

Aphrodite should route future monitoring stats through Silver
`MetricObservation` and `MetricRollupObservation` records with explicit recipe
versions, source observation ids, posture/value coupling, sample support,
freshness, and limitations. That includes any future:

- moving average;
- exponential moving average (EMA);
- compatible-window velocity;
- spike score;
- breakout state;
- decay or plateau state;
- active-watch expiry state.

Do not compute those inside `creator_profile_current` as hidden product logic.
Silver owns the recipe-backed observations and rollups; the registry/profile
current view copies only accepted, lineage-backed fields.

## Strategy Calls

1. Use daily grid heartbeat as the registry currentness layer once budget and
   platform posture are accepted.
2. Use event-triggered promotion for ongoing first deep capture: spike or fresh
   breakout. Buyer relevance is a label/priority, not a hard pre-gate; active
   breakout is a metric-recheck trigger, not repeat deep capture by default.
3. Treat views plus engagement as the default selection basis.
4. Treat fallen-out unpromoted content as cold by default.
5. Preserve promoted breakout exceptions with one or two explicit metric-only
   rechecks, read caps, age caps, and expiry.
6. Keep control/edge creators in the registry at low cadence or test-window
   cadence, not as a daily deep-monitoring burden.
7. Keep fragrance depth as the wedge, but include fragrance-proven adjacent and
   control creators so the signal learns both yes and no.
8. Keep Studio/activation downstream of Signals. The capture strategy exists to
   sharpen Signals first.

## Open Decisions Before Calculation

These must be decided or measured before computing realistic roster size:

- Whether Aphrodite accepts daily grid heartbeat as the target posture, replacing
  the current more conservative IG C-tier heartbeat assumption for this vertical.
- Measured request cost for one grid heartbeat per platform/account.
- Expected daily new-content rate per creator.
- Expected promotion rate from grid heartbeat into deep capture.
- Deep-capture cost per promoted item by platform and source surface.
- Maximum deep captures per creator per day.
- Breakout recheck schedule, metric-only recheck count, decay threshold, and
  expiry rule.
- Whether visual/OCR or thumbnail interpretation deserves a separate measured
  evidence lane after the cheap heartbeat route is characterized.
- Which Silver metric recipes should be documented first: moving average, EMA,
  compatible-window velocity, spike score, breakout state, or decay state.
- Roster composition bands: fragrance-core, fragrance-proven adjacent, and
  control/edge.
- Control/edge cadence and promotion rule.

The later calculation should use:

```text
daily_cost =
  registry_creator_count * grid_heartbeat_cost
  + onboarding_creator_count * onboarding_grid_and_deep_cost
  + promoted_content_count * deep_capture_cost
  + active_breakout_count * breakout_recheck_cost
```

Do not calculate from vibes. Use measured request counts, observed promotion
rate, and explicit safety stop conditions.

## Non-Goals

- no live capture authorization;
- no scheduler, daemon, crawler, or standing passive discovery authorization;
- no proxy, account-rotation, or bot-detection evasion plan;
- no final 2.5k-3k roster claim;
- no buyer proof or product readiness claim;
- no outreach, lead-list, contact, or creator-representation workflow;
- no public person identity, demographic, follower graph, or contact enrichment;
- no claim that deep capture creates performance guarantees;
- no action recommendation from Silver alone.
