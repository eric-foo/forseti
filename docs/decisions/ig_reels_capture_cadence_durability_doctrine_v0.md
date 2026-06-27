# IG Reels Capture Cadence And Durability Doctrine (v0)

```yaml
retrieval_header_version: 1
artifact_role: capture-ops cadence/durability design proposal (non-authorizing)
scope: >
  How to run the public IG `/reels/` capture at scale over time for creator-traction
  monitoring: a rate/cadence budget, transient-vs-block response policy, graceful
  degradation, and honest gap recording. Operate within platform limits and fail
  honestly; this is NOT stealth, anti-detection, or evasion guidance.
use_when:
  - Scoping a scheduled multi-creator reels monitoring panel.
  - Deciding retry/backoff and degradation behavior around the per-invocation runner.
  - Checking what produces the timepoints the downstream momentum/Spike-Alert lane consumes.
open_next:
  - orca/product/spines/capture/core/source_families/social_media/instagram/ig_profile_grid_dom_engagement_recon_and_spec_v0.md
  - docs/workflows/ig_reels_capture_to_projection_ecr_cleaning_handoff_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
authority_boundary: retrieval_only
status: PROPOSAL_RECORDED_V0
stale_if:
  - The per-invocation runner stops returning typed block/transient exit codes.
  - An owner decision selects a scheduler/runtime, which this note does not.
  - The data-lake scheduling/retry exclusion boundary changes.
```

## Status

`PROPOSAL_RECORDED_V0`. This is a design note, not implementation authority, validation,
readiness, scheduler/runtime selection, or a platform-stability claim. It records the "how"
asked for during the 2026-06-25 IG reels capture lane work; it does not build the scheduler.

## Problem

A **single** `/reels/` capture is already complete and honest: the runner either writes a
clean packet or **fails closed** -- `_detect_ig_block` returns a typed reason (login redirect,
429 "please wait" interstitial, "you've been blocked", challenge route) and the run exits
without writing a garbage packet (exit `5`); runner/capture failures exit `3` for bounded
retry; CLI/configuration failures exit `2` and are not retry cadence events. What is missing
is the **durability envelope** for running this repeatedly across many creators to produce
the momentum timepoints: how often, how spaced, what to do on a soft failure, and how to
degrade without either hammering the platform or silently dropping data.

This matters because momentum is built from **per-timepoint deltas**, and a timepoint missed
or corrupted at capture time is a **permanent** hole in that creator's series.

## Ownership

This is a **new ops/scheduler lane**, owned by neither Capture nor the Data Lake:

- The Data Lake core contract explicitly **excludes** "downstream scheduling, retry, completion
  gating". The lake only retains write-once raw timepoints and offers them by key.
- The capture runner is **per-invocation** by design and already fails closed; it must stay that
  way (no scheduling/retry inside the runner).

The durability layer is therefore a **thin wrapper around the unchanged runner** plus this
operating doctrine.

## What it is NOT

This is rate-respect and honest degradation, **not** stealth, fingerprint, anti-detection, or
account-evasion guidance. The goal is to operate **within** platform limits and surface failure,
not to circumvent limits or hide automation. Block detection stays a fail-closed honesty
mechanism, never an evasion trigger.

## Design (smallest-complete first)

1. **Rate / cadence budget (doctrine, low lock-in -- do first).**
   - A declared budget: capture throughput, minimum spacing between captures, and a
     per-creator re-capture interval (the monitoring cadence). The cadence is the knob that
     sets how dense each creator's momentum series is; pick it per the decision question, not
     maximally.
   - Recorded as configuration/doctrine, not hard-coded into the runner.
   - Concrete owner-set v0 values: see **v0 Cadence Budget** below.

2. **Transient-vs-block response (reads the signals already emitted).**
   - Exit `5` (access block: login redirect, 429 interstitial, network-security block, or
     challenge route) -> back off that creator/panel; do **not** immediately retry, retry
     harder, or route around the block. Widen spacing or pause the run. A hard block is a
     rate signal to slow down, never a prompt to force the missing timepoint.
   - Exit `3` (runner/capture failure: timeout, browser/launch error, or surfaced runtime
     exception) -> bounded retry with backoff, capped attempts; if the cap is exhausted,
     record the scheduled timepoint as a gap.
   - Exit `2` (CLI/configuration error) -> stop the wrapper for operator correction; do not
     consume retry budget or fabricate a monitoring observation.

3. **Graceful degradation.**
   - On a block mid-panel, slow or pause the remaining panel rather than continue at speed.
   - A skipped or blocked creator records an **explicit gap** for that timepoint (so the series
     carries an honest hole), never a silent omission and never a fabricated value. If the
     runner did not write a raw packet, the gap record is not a fake `SourceCapturePacket`
     value; it must carry the planned creator/timepoint plus the observed outcome/reason.

4. **Thin scheduler wrapper (higher lock-in -- do when a real panel is scheduled).**
   - Enforces 1-3 around the per-invocation runner. The runner itself is unchanged.
   - This is the durable workflow-shape piece; defer it until a concrete panel run justifies the
     lock-in. Until then, the budget doctrine + the runner's existing fail-closed behavior are
     enough for ad-hoc monitoring.

## v0 Cadence Budget (owner-set 2026-06-26)

Concrete v0 values for Design rule 1, set by the owner. They supersede "cadence numbers
deferred" for the cadence knobs only; scheduler/runtime selection and the gap-record storage
home stay deferred. These are starting values to operate and tune against observed block
rate, not a platform guarantee or a final lock.

- **Active window:** captures run across **three ~4h active sessions (~12h active/day total),
  with breaks between sessions**, NOT 24/7. The cap is therefore NOT `panel_size / 24h`;
  throughput is bounded by the active-time x average-spacing ceiling below.
- **Spacing:** **~30 seconds average** between captures, **jittered per gap** (each gap drawn
  from roughly a **15-45s window**) so the schedule is an average rate with natural variance,
  not a fixed interval. The **average** -- not a floor -- is what sets throughput.
- **Per-creator interval (two tiers):**
  - **Tier 1 baseline:** **1x/day** for every creator. This yields spike *detection* at roughly
    one-day latency -- a jump shows at the next daily capture.
  - **Tier 2 escalated:** **2-4x/day**, only for creators with an active Spike Alert. This
    *tracks* a spike once detected; de-escalate when the creator returns to usual range.
- **Throughput ceiling (derived, not a separate knob):** `active_time / avg_spacing` =
  `12h x 3600 / 30s` = **~1,440 captures/day** across the three sessions.
- **Capacity vs. panel size:**
  - A 1x/day baseline fits comfortably up to ~**1,150 creators** in the 12h / 30s-average
    budget (~20% headroom for Tier-2 escalation).
  - The **1,000-creator target fits** the v0 budget: 1,000 baseline = `1000 x 30s` = 8.3h
    active (~69% of the 12h), leaving ~**440 captures/day** of headroom for Tier-2 escalation.
    Beyond ~1,150 creators, relieve by **adding session time** or **splitting the panel** --
    NOT by dropping the average spacing.

**Spike model (explicit accepted limit).** Real-time spike catching is out of reach: it would
require hourly monitoring of the whole panel, which does not fit the window/spacing budget at
1k. The accepted model is **detect-then-escalate**: the Tier-1 daily baseline detects a spike at
~1-day latency (via the downstream Spike-Alert lane), which flags that creator for Tier-2
escalation; the escalation pool stays small (only currently-flagged creators), so it fits in the
headroom. Loop: cadence -> daily timepoints -> Spike-Alert detection -> Tier-2 flag back into
cadence.

## Relationship to the rest of the pipeline

The durability layer produces successful capture **timepoints** plus explicit gap records for
scheduled observations that did not produce raw packets. The Data Lake **retains** successful
raw packets write-once and serves them by key; a downstream **pre-gold momentum/Spike-Alert
lane** diffs raw-keyed observations and carries missingness as missingness into "usual-range
threshold crossed" candidate records keyed to raw; **Judgment** alone interprets those (gold).
Durability is upstream of all of that -- it only governs how scheduled timepoints are
attempted, slowed, paused, or recorded as gaps.

## Open owner decisions / blockers

- The concrete cadence numbers are now **set as owner v0 (2026-06-26)** -- see "v0 Cadence
  Budget" above. They are starting values to tune against observed block rate, not a final
  lock. The 1k target fits the v0 12h budget (~69% utilization); beyond ~1,150 creators, add
  session time or split the panel.
- Scheduler/runtime selection -- deferred; not chosen here.
- Whether the gap-recording home for a skipped/blocked timepoint is a capture-side artifact or
  a downstream-series-side annotation -- resolve when the momentum lane is scoped. The
  obligation to record the gap and its minimum planned-timepoint/outcome/reason contents is not
  deferred.

## Non-claims

- not validation
- not readiness or production-fitness
- not scheduler/runtime/backend selection
- not a platform-stability or block-rate guarantee
- not stealth, anti-detection, or evasion guidance
- not a momentum, demand, credibility, or Judgment claim
- not a retry policy for configuration/usage errors
