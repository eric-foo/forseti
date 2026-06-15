```yaml
retrieval_header_version: 1
artifact_role: proposed architecture (non-authorizing) — creator monitoring policy (coverage allocator)
scope: >
  The monitoring policy for the Orca creator-momentum capture→projection lane: how a bounded capture
  budget (R safe reads/day, ≤10 attended operating accounts start ≤5) is allocated across an UNCAPPED
  subject roster so the momentum / wind-calling signal gets the most coverage. Defines the
  platform-AGNOSTIC core machinery (tier model, age-bucket scheduler, per-creator cap, virality
  hot-list, promotion/demotion loop, capture-once-then-recheck lifecycle) and the per-platform
  monitoring PROFILE seam (cadence values, curve window, content unit, momentum metric, spike
  threshold) that IG fills first and TikTok/YouTube/Reddit fill later. PROPOSED; the cadence numbers
  are illustrative and R-tunable (R is unmeasured). Not a build-go, validation, or readiness claim.
use_when:
  - Deciding how to spend the bounded capture budget across creators/posts (tiering + recheck cadence).
  - Scoping the IG capture-shape contract's monitoring half, or a future platform satellite's profile.
  - Checking what monitoring machinery is platform-agnostic core vs per-platform satellite.
authority_boundary: retrieval_only
open_next:
  - docs/product/data_capture_spine/orca_capture_projection_storage_spine_architecture_v0.md   # the storage/capture-shape backbone (this consumes its projection + records its cadence/fanout parameters)
  - docs/decisions/wind_caller_calibration_carveout_v0.md   # capture posture authority (amended 2026-06-15) — the scheduler must conform
  - docs/product/data_capture_spine/orca_creator_momentum_pipeline_architecture_v0.md   # the IG-first pipeline instance
stale_if:
  - The owner adopts/adjusts the tier model, the age-bucket scheduler, or the carve-out conformance posture.
  - R is measured (the rate-limit probe lands) — turns the illustrative cadences into sized defaults.
  - The IG capture-shape contract fills the IG monitoring profile (moves IG from illustrative to bound).
  - A second platform profile (TikTok/YouTube/Reddit) is authorized — tests the profile seam.
status: PROPOSED — creator monitoring policy (core machinery + per-platform profile seam); cadences illustrative + R-tunable; AWAITING owner adoption
```

# Orca Creator Monitoring Policy — Coverage Allocator (PROPOSED, v0)

## Result

The monitoring policy is **how a bounded capture budget is allocated across an uncapped roster so the
momentum signal gets the most coverage.** It is a **platform-agnostic core scheduler/allocator
parameterized by a per-platform monitoring profile.** "Full-vertical coverage" is achieved not by
monitoring everyone at full density (throughput forbids it) but by **tiering density by signal**:
everyone is on the radar via a cheap heartbeat; the read budget concentrates where the momentum /
wind-calling signal is.

## Core vs satellite split

- **CORE (platform-agnostic; this doc):** the tier model (A/B/C), the age-bucket scheduler structure,
  the per-creator concurrently-tracked cap, the virality hot-list, the promotion/demotion loop, the
  capture-once-then-recheck lifecycle, and the read-budget allocation rule. A reusable allocator that
  **takes parameters**.
- **SATELLITE (per-platform monitoring PROFILE; the parameters):** the curve-window length, the
  age-bucket boundaries + cadences, the per-creator cap, what a "post" / content-unit is, which metric
  defines momentum (and its unit), the spike threshold + its normalization, the typical posting-frequency
  prior, and the heartbeat cadence. IG fills these first (in the IG capture-shape contract); TikTok /
  YouTube / Reddit fill them later as **named-deferred** seams.

The platform *differences* are entirely satellite values, **not new machinery**: YouTube's months-long
view curves + low posting frequency, or TikTok's delayed-FYP virality, are *different profile values*
feeding the *same* core scheduler — not a different scheduler.

## Tier model (core)

| Tier | Who | Coverage |
|---|---|---|
| **A** | high-signal: rising micro/mid, active wind-callers | full age-bucket curve density |
| **B** | established / slow | follower-trajectory + sampled posts (catch band-jumps, not every post) |
| **C** | long tail / dormant | a cheap periodic follower/subscriber **heartbeat** (detect a rise → promote to A) |

Everyone in the enumerated roster is at least Tier C (on the radar); the budget concentrates on A. This
is full-vertical coverage in the sense that matters: known + watched everywhere, dense where the signal is.

## Age-bucket scheduler (core structure; satellite values)

Each tracked post is sampled on a cadence that **decays with the post's absolute age** (NOT its recency
rank — rank misallocates for sporadic and hyper-prolific posters). Posts migrate to sparser buckets as
they age out of the curve window.

- **Per-creator cap:** at most ~K posts per creator are *concurrently curve-tracked* (top-K by recency);
  overflow gets **baseline-only**. This bounds the per-creator read load regardless of posting rate.
- **IG profile values (illustrative; R-tunable):** age `0–5d` → daily · `6–15d` → every 3d · `16–30d`
  → weekly · curve window 30d · per-creator cap K≈30. (A daily poster fully tracked ≈ ~10 reads/day; a
  density dial to set against measured R.)

## Virality hot-list (core machinery; satellite threshold)

Any post (or creator) whose key metric **spikes** between samples is promoted to a **tight cadence**
(e.g. `6h / 12h`) regardless of its age bucket, until the spike resolves. The spike *detector* (velocity
of the key metric) is core; the **threshold + its normalization is a satellite value** (velocity is
platform-shaped). This is adaptive density catching momentum in flight.

## Promotion / demotion loop (core)

A Tier-C heartbeat catching a follower/subscriber jump **promotes** the creator to Tier-A density;
fading momentum **demotes** back toward C. The momentum signal — the product's core read — thus does
**double duty as the coverage allocator**: the thing we are trying to detect is the thing that decides
where to spend the budget.

## Capture-once-then-recheck lifecycle

1. A new post is **captured once at discovery** (the baseline observation; one feed/profile poll detects
   all new posts since the last check).
2. The post then enters the **age-bucket scheduler** (above) for its recheck curve.
3. **Adaptive density:** baseline *every* post cheaply; spend full-curve density only on the signal
   (Tier-A creators and/or spiking posts). Routine posts get baseline + one follow-up; breakouts get the
   full curve. "Full curve on everything" is the budget trap.

## Read-budget equation + the R dial

```
reads/cycle ≈ Σ_creators [ Σ_buckets (tracked_posts_in_bucket / bucket_cadence) ]
                       + new-post polls + Tier-C heartbeats
bound: reads/cycle ≤ R × cycle_days     (R = safe reads/day — UNMEASURED key unknown)
```

The bucket cadences and the per-creator cap are **R-tunable dials**, not fixed truths. **R is the one
empirically-unmeasured number** (a bounded rate-limit probe resolves it). R sizes *Tier-A breadth*
(how many creators get full density), **not** the storage tier — total rows stay throughput-bounded
(10⁷–10⁸ over the working horizon → no server; see the storage backbone).

**Batching note:** polling an age bucket reads its posts **together** → the reads return as a batch →
the batch materializes as one projection partition. So the scheduler naturally produces the
single-writer **batch** write pattern the storage backbone wants (captures write packets per-read;
the columnar projection is a low-frequency batch derivation — no high-frequency DB writes, no contention).

## Per-platform monitoring profile (the satellite seam)

Each platform satellite fills this profile; the core scheduler consumes it. **IG filled (illustrative);
others named-but-NOT-filled.**

| Profile field | IG (illustrative) | TikTok (deferred) | YouTube (deferred) | Reddit (deferred) |
|---|---|---|---|---|
| content unit | reel / post | video | video | post/comment |
| momentum metric (unit) | view_count (count) | play_count (count) | view_count + watch_time (count/sec) | score/upvotes (signed) |
| curve window | ~30d | longer / less predictable (delayed FYP virality) | **months–years** (long-tail search/suggested) | hours–days |
| age-bucket cadences | 0–5d daily / 6–15d 3d / 16–30d weekly | TBD | **much sparser, longer horizon** | TBD |
| per-creator cap K | ~30 | TBD | TBD (low — few uploads) | TBD |
| posting-frequency prior | ~daily | high | **low (weekly)** | varies |
| spike threshold/normalization | TBD | TBD | TBD | TBD |
| heartbeat cadence (Tier C) | ~weekly | TBD | TBD | TBD |

YouTube is the sharpest proof of the seam: its **months-to-years** curve window + **low posting
frequency** are *profile values*, handled without touching the core scheduler.

## Carve-out conformance (load-bearing — must not become a standing crawler)

The carve-out (amended 2026-06-15) permits passive monitoring only as **human-initiated, time-bounded,
self-terminating** sessions — **no perpetual/scheduled standing crawler.** So:

- The cadences here define an **ideal sampling schedule (a target)**, executed by **batching the due
  reads into bounded attended monitoring sessions** — NOT a 24/7 daemon that auto-fires every 6h. A
  sample "due at +6h" is taken whenever the next bounded session runs.
- **Resolved (owner, 2026-06-15 — posture (C), v0):** virality uses **best-effort-within-session**. The
  hot-list *flags* spiking posts (spike detection = reading the projection, always permitted), and the
  tight 6h/12h sampling happens whenever the next bounded session runs — **no sprint mechanism and no
  carve-out amendment for v0.** Tight cadences are *best-effort targets, not guarantees*; coarser peak
  resolution is accepted for v0. Escalation path if best-effort proves too coarse to capture the
  wind-calling moment: **(A)** human-initiated bounded sprints (still conformant), then **(B)**
  pre-authorized supervised-autonomy auto-launch (would need a dated carve-out clarification) — both
  **deferred, not built.**
- Account-cap rules (≤10 / start ≤5 operating accounts) apply to social platforms; EDGAR/org-motion (if
  ever monitored) is a separate non-person posture, not governed here.

## Non-claims

PROPOSED monitoring-policy architecture only — not a build-go, validation, readiness, or authorization.
All cadence/cap numbers are **illustrative and R-tunable**; R is unmeasured. Core machinery here; IG
profile values are finalized in the IG capture-shape contract; other platform profiles are
named-deferred seams. The scheduler consumes the rebuildable projection (the storage backbone) and must
conform to the carve-out's bounded-session posture.
