# IG R-Probe — Results (v0, first measured reading)

```yaml
retrieval_header_version: 1
artifact_role: probe results / measured findings (non-authorizing; n=1 onset — directional, not fully characterized)
scope: >
  First live measured reading of per-IP R (logged-out IG safe reads) + rate-limit-onset
  behavior for the IG creator-momentum path, from the bounded probe designed in
  ig_sustained_cadence_r_probe_design_v0.md. Headline: the binding constraint is per-IP
  PACE, not session volume; a sub-2s burst trips an IP-wide soft login-wall; proper pacing
  (>=~2s) sustained 176 modeled requests with no wall. Reports for two consumers and gives
  the proxies-vs-sessions-vs-neither call, plus two recovery-gated endurance attempts that
  did not measure the at-pace ceiling.
use_when:
  - Reading the measured R result before sizing monitoring cadences or the projection-store engine.
  - Checking whether proxies / IP-rotation / sessions are warranted (the conditional fork).
  - Planning a fuller R characterization (pace threshold, volume ceiling at pace, throttle decay).
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_sustained_cadence_r_probe_design_v0.md   # the method this measures
  - forseti/product/spines/capture/core/source_families/social_media/instagram/orca_creator_monitoring_policy_architecture_v0.md   # Consumer A (cadence sizing)
  - docs/decisions/wind_caller_calibration_carveout_v0.md   # capture posture authority
stale_if:
  - A fuller run pins the pace threshold, the at-pace daily-volume ceiling, or the throttle decay time.
  - The burst (6h/12h) profile is actually run (this result infers it is safe; not yet measured).
branch_or_commit: measured against origin/main @ f266f83b base; instrument = run_source_capture_ig_calls_packet.py (logged-out). Raw: forseti-harness/_test_runs/r_probe/{ramp,ramp2,disambig,endurance,endurance2}/ (gitignored; endurance2 has log only, no summary file).
```

## Status
`RESULTS — FIRST MEASURED READING (n=1 onset + 3-read disambiguation; two failed recovery-gated
endurance attempts).` Directional and well-supported, but **not** a fully-characterized R.
Logged-out, attended, bounded; the IP was throttled at the end, and later endurance attempts did
not clear the warm-up gate. Not validation/readiness.

## What ran (two sessions + disambiguation + recovery attempts)
| Session | Pace | Reads | Onset |
|---|---|---|---|
| **Run 1** (harvested after a crash) | R1+R2 (8–45s → 2–8s gaps) | 143 reads / **~176 modeled IG-requests**, 5 creators, 37 min | **NONE** |
| **Run 2** (R2→R3) | R2 then R3 (0.5–2s gaps) | 6 invocations / ~84 modeled | **ONSET** `redirected_to_login` on the **first R3 read** (`kayla.ryan1`) |
| **Disambiguation** (gentle, post-onset) | 6–12s gaps, 1 item | `kayla.ryan1`→**recovered (rc 0)**; `theglownarrative`→**blocked**; `milkydew_`→**blocked** | IP-wide, soft |
| **Endurance attempt** (later; recovery-gated, 8 creators) | warm-up probes every ~150s | 5 recovery attempts over ~12.7 min — never both-clean (1 lone slip-through @ ~5 min) | **ABORTED `ip_not_recovered`** — at-pace ceiling NOT measured; throttle still active |
| **Endurance retry 2** (later; recovery-gated) | warm-up probes roughly every 10–11 min | 3 recovery attempts over ~21.6 min — never both-clean (attempt 1: 1 clean + 1 blocked; attempts 2–3: both blocked) | **NO CEILING MEASURED** — no `endurance_summary.json` was written; only `endurance_log.jsonl` exists |

## Finding — the limit is PACE, not volume
- **Run 1 did 176 modeled requests at ≥2s pace with zero walls; run 2 walled the instant it went sub-2s.** Volume isn't the binding constraint (run 1 = 2× run 2's volume, gentler, clean). **Pace is.**
- The wall is **IP-wide** (two distinct creators blocked in the disambiguation), **soft** (`kayla` recovered one read → not a ban), and presents as **`redirected_to_login`** (IG's logged-out throttle mechanism — *not* a `429`).
- Once a sub-2s burst trips it, the throttle is **sticky**: it persisted **≥12 min** under gentle periodic probing (every ~150s), with only occasional single-read slip-throughs; a later retry still did not produce two clean warm-up reads over ~21.6 min. The probing itself may sustain the state. Full recovery needs a longer **fully-quiet** cooldown (>21 min, unmeasured). *(Corrects an earlier "decays in minutes" reading — the endurance attempts' recovery gates never cleared.)*
- Per-creator read cost ≈ **16 modeled IG-requests** (1 profile≈4 + 12 items); call-yield ≈ **~89%** (image-carousel posts whose `og:description` lacks engagement miss the signal — not a block).

## Report — two consumers (per design Delta 2)
1. **Steady-state R (Consumer A — monitoring policy):** no daily-volume ceiling found; ≥176 modeled/session is clean **at ≥~2s inter-read spacing**. Cadence sizing should treat R as **pace-bound**: space batched reads **≥~2–4s, never sub-2s**. The policy's realistic cadences (daily / 3-day / weekly per post, batched) are far gentler than the pace that trips the wall → safe.
2. **Burst-cadence feasibility (de-risks (B)):** **inferred SAFE, not yet run.** A 6h/12h sprint reads hours apart — orders of magnitude gentler than the sub-2s pace that trips the throttle. The pace wall is about *rapid-fire* reads, not 6h-spaced ones. (Still worth a confirming attended run.)
3. **Roster size:** all-in-vertical `M` is a discovery-lane output, not measured here (the snowball found sub-niche communities converge — 243 uniques from 15 reads in fragrance). Use the policy's illustrative M≈200–1000.
4. **Per-platform read cost (Consumer B — projection-store):** IG ≈ 16 modeled requests / full creator read, ~89% yield. Reads are pace-limited (not volume-limited) and the projection is a low-frequency batch derivation → supports the storage backbone's existing **throughput-bounded / no-server** conclusion. Engine pick is **not gated by a volume problem** here.

## Decision — proxies vs sessions vs neither
**NEITHER proxies/IP-rotation NOR re-opening the sessioned lane is warranted** for the realistic
monitoring + burst cadences. The binding constraint is **per-IP pace**, and the operative
mitigation is **pace discipline** (space reads ≥~2–4s; no sub-2s bursts; bounded attended
sessions). This is decision-rule **branch 1 (no scaling mitigation needed)** with a pacing
refinement — *not* branch 2/3.

- Proxies would only help if we needed sustained **sub-2s throughput**, which no monitoring/burst
  cadence requires.
- Sessions (account-keyed) trade the pace-throttle for ban-risk + ToS + a carve-out amendment —
  unjustified when pace discipline already clears the realistic load.

## Owner closeout (2026-06-16)
Owner-accepted on this reading:
- **Operating pace target ≈ 2.5–4s between reads** — a safety margin above the ~2s trip point; at
  this pace the probe read sustained (run 1: 176 modeled / 37 min, no wall). Beyond that spacing,
  expect long clean read sessions.
- **Burst (B) confirming run — WAIVED** (owner: safe for sure); 6h/12h is far gentler than the pace
  that trips the wall.
- **Fuller characterization (pin the pace threshold + at-pace daily-volume ceiling) — DEFERRED** to a
  future contingency, to run **only if we hit a persistent / perma block** (the unpinned at-pace
  ceiling is the open risk that would matter then).

Lane core question (report R + decide proxies) is **ANSWERED**: R is pace-bound; neither proxies nor
sessions are warranted; operate at ~2.5–4s spacing in bounded attended sessions.

## Caveats / residuals (why this is directional, n=1)
- **Pace threshold not pinned** — we know ≥2s clean and sub-2s trips it; the exact boundary (1s? burst-shape?) is unmeasured.
- **At-pace daily-volume ceiling not pinned** — clean to ≥176/session; two recovery-gated endurance attempts did not reach the at-pace phase. The per-day ceiling at proper pace and the throttle's decay time are still unmeasured. If all-in-vertical `M` is very large, re-check volume at proper pace after a long fully-quiet cooldown.
- **Onset is a single event** (`redirected_to_login`, not a `429`); the disambiguation supports IP-wide + soft, but a repeat run would harden the reading.
- **Burst profile inferred, not run.**

## Non-claims
First measured reading only — not validation, readiness, buyer-proof, or commercial authorization.
Figures are from logged-out attended probe runs (raw in gitignored `_test_runs/`), n=1 onset; the
second endurance retry is log-only because the expected summary file is absent.
"Safe"/"clean" describe observed probe behavior at the tested pace/volume, not a guarantee.
