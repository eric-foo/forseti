# Forseti Research Engine — God-Tier Target v0

```yaml
retrieval_header_version: 1
artifact_role: Decision record (owner-set capability target; north-star definition, not a readiness claim)
scope: >
  The durable "god tier" bar the research engine (CSB, Scanning, Capture) is
  built toward. Scoped to the three extraction spines and their two internal
  seams (CSB->Scanning, Scanning->Capture) plus the Capture->ECR handoff as a
  boundary obligation. ECR and everything downstream are out of scope by owner
  direction (see the ECR-onwards deferral record). Names the capability bar,
  the measurable done-conditions, and the accepted residuals.
use_when:
  - Deciding whether a proposed research-engine investment moves toward or past the target.
  - Checking the god-tier done-conditions for CSB, Scanning, or Capture.
  - Auditing whether a "god tier" claim on the research engine named its accepted residuals.
authority_boundary: retrieval_only
open_next:
  - docs/research/forseti_research_engine_god_tier_strategy_v0.md   # the weakness map + phased plan toward this target
  - docs/decisions/forseti_research_engine_ecr_onwards_deferral_v0.md   # why the target stops at the ECR handoff
  - docs/decisions/forseti_mini_god_tier_doctrine_v0.md   # the MGT lens this target is calibrated against
  - docs/workflows/forseti_research_engine_map_v0.md   # the three-spine grouping this targets
  - docs/decisions/forseti_icp_wedge_consumer_demand_first_v0.md   # the product direction the target must serve
stale_if:
  - The ratified product direction (consumer-demand, >=2 independent venue families, 30-90 day window) is superseded.
  - A spine joins or leaves the CSB -> Scanning -> Capture group, or the Capture->ECR boundary moves.
  - A later owner decision amends or supersedes this target.
```

## Status

`OWNER_SET_TARGET_V0` — owner-directed 2026-07-10 on the research-engine
strategy lane ("write down GT into a durable artifact for us to strive for").
This is a capability-target lens and a north star, not validation, readiness,
or proof. Nothing here asserts any listed condition is met; the companion
strategy record holds the current (largely unmet) baseline.

Scope is **research engine only**. ECR, Cleaning, Judgment, buyer proof, and
run authorization are out of scope by the same owner turn; see
`docs/decisions/forseti_research_engine_ecr_onwards_deferral_v0.md`. The
Capture->ECR handoff appears here only as a *boundary obligation* the engine
must discharge, never as downstream work this target owns.

## Calibration Against Mini God Tier

This is the **full god-tier** bar the engine is built toward — a north-star
target, not a readiness claim, and not the bounded slice we stop at this
quarter.
Under the Mini God Tier doctrine
(`docs/decisions/forseti_mini_god_tier_doctrine_v0.md`), individual
interventions toward this target may consciously stop at ~90-95% and name their
residuals; the phased plan in the strategy record is where that MGT slicing
happens. The two compose: this record sets the TARGET; Smallest Complete
Intervention governs each step toward it; MGT decides how far each step pushes.
Labeling the engine "god tier" is void unless the accepted-residuals section
below is honored.

## The One-Line Target

**Any commissioned decision question turns into fresh (30-90 day),
provenance-hashed, multi-venue-family evidence — preserved and ECR-handoff-ready
— in hours-to-days, at case-batch scale, with coverage that compounds run over
run and cost that measures itself, all inside the evidence-grade,
no-overclaim discipline that is the moat.**

If the engine cannot do this, it is not yet god tier — regardless of how much
capability doc exists.

## God Tier, Per Spine

### CSB (decide what to look for) — god tier

- A commission is generated from a decision question in one bounded pass, and
  its board **compounds**: a regenerated board inherits prior rows and their
  last-known evidence status rather than starting blank and expiring.
- Every board row carries an explicit gate role and demand-origin family, so
  Scanning knows what a "second independent venue family" would even be.
- Board output shape is mechanically checked at the boundary that matters
  (not merely available as a manual command), and the check resolves the board
  it claims to cite rather than trusting a string.
- CSB stays evidence/signals-only — it never emits gate verdicts. (Unchanged
  boundary; god tier does not relax it.)

### Scanning (discovery) — god tier

- A scan reliably tests CSB rows across **>=2 independent demand-origin venue
  families**, not one, and records why a family was reachable or not.
- Hidden-venue discovery and exact-query discipline produce *new* venues run
  over run, drawing on compounding route/venue memory instead of rediscovering
  the same handful each time.
- Every `capture_request` a scan emits enters a **tracked lifecycle** and
  reaches a terminal state (fulfilled / declined-with-reason) — no request dies
  as `route_binding_state: unknown`.
- "Blocked" is never a reflex: recording a venue blocked requires a mode-ladder
  receipt (which access modes were tried, or an explicit skip reason), enforced
  at the boundary, so the dominant historical false-diagnosis cannot recur
  silently.
- Each scan emits a cost/yield row (tokens, wall-clock, venues touched,
  candidates produced) so scanning is optimizable and pricable.

### Capture (acquisition) — god tier

- Every proven source family (fragrance-native DB, retail/PDP, vendor pricing,
  IG, TikTok, YouTube, Reddit, and the demand-origin forums the vertical needs)
  captures on demand into a schema-valid, hash-provenanced packet, with a
  shared controlled route-state vocabulary saying exactly how proven each
  route is.
- Demand-origin forums (buyer-language communities, fragrance DBs) — the
  highest-signal, historically hardest class — are first-class proven routes,
  not perennial blocked entries.
- A commissioned batch of capture_requests runs through **one orchestrated
  entrypoint** with per-lane isolation, budget caps, and receipts — not 90-odd
  scripts invoked by hand — while staying commissioned-batch, never a standing
  crawler.
- Every proven route is live-smoked on a cadence so route rot is caught before
  a commissioned run hits it, and one golden packet per family is fixture-
  admitted so the discipline is testable.
- The Capture->ECR handoff obligation (inspectable, preserved-or-limits-visible,
  claim/interpretation separated, identity/timing/cutoff/archive posture
  present) is discharged and **mechanically verifiable at the boundary**, so a
  packet is provably handoff-ready without asserting anything about downstream
  ECR behavior.
- Every capture run emits a cost/yield row, feeding an engine-level "dollars and
  hours per evidence-unit" readout.

## Measurable Done-Conditions (baseline -> target)

These are the gates that decide whether the bar is met. Baselines are as
observed 2026-07-10 in the strategy record.

1. capture_request terminal-state rate: **0% -> 100%**.
2. Demand-origin venue families captured per commissioned case: **~1 -> >=2**
   (ratified floor), 3+ at the top of the bar.
3. Commission -> ECR-handoff-ready latency: **never measured -> baselined ->
   <=2 days -> hours**.
4. Runs emitting a cost/yield row: **0% -> 100%**.
5. Proven routes live-smoked within 7 days before commissioned use:
   **no live coverage -> standing opt-in smoke tier**.
6. New-scan venues pre-known from route/venue memory vs rediscovered:
   **unmeasured -> rising**.
7. Capture->ECR handoff obligation mechanically verified (not prose self-check):
   **0 -> enforced at the boundary**.
8. Demand-origin forums as proven routes: **~1 (Fragrantica, once) -> the set
   the vertical needs**.

Percentages are target calibration, not achievement claims; report a number
only with independent evidence.

## Accepted Residuals (mandatory; named, bounded, upgrade-triggered)

Per the Mini God Tier doctrine, these are consciously accepted now:

- **LinkedIn stays policy-blocked.** Professional-context evidence has no built
  capture route. Accepted because the vertical is consumer-demand, not B2B.
  Upgrade trigger: a written-permission route, or a vertical shift that needs
  professional context.
- **Headless SERP stays parked; SERP is operator-attended.** Headless was 100%
  bot-blocked; only a visible browser worked. Accepted because a visible-browser
  route exists. Upgrade trigger: a materially different access posture — not
  more headless retries.
- **Durable media/video preservation on IG/TikTok is unproven.** Metadata/text
  layers carry the signal today. Accepted because text/metadata answer most
  demand questions. Upgrade trigger: a commissioned decision that turns on the
  video/image bytes themselves.
- **Live-network checks stay opt-in / operator-triggered, never default CI.**
  Accepted because account safety outranks detection latency. Upgrade trigger:
  a sanctioned, low-risk endpoint set safe for unattended cadence.
- **Standing cadence, if adopted, is narrow and budget-capped** (named
  recurring families only), never a broad autonomous crawler. Accepted as the
  boundary between god-tier throughput and the rejected always-on-collector
  shape.

An unlisted capability drop voids the "god tier" label for the engine.

## Anti-Goals (god tier is explicitly NOT)

- A broad crawler, standing monitor, or venue atlas-as-authority.
- CAPTCHA-solving, login automation, cookie import, or commercial scraping
  services (the Armory gated list stands).
- Dashboards or UI before the loop closes.
- New doctrine layers before execution volume — doctrine is the over-supplied
  asset; execution is the bottleneck.
- Any ECR / Cleaning / Judgment / buyer-proof capability — out of scope by
  owner direction.

## Non-Claims

Sets a capability target and vocabulary only. Authorizes no build, capture,
source access, scaling, scheduling, or run. Not validation, not readiness, not
proof, not a numeric achievement claim, and not authorization for any code
root. Reaching any condition above requires its own work, verification, and
the normal per-lane authorization and review flow.
