# IG Capture Rate — Preliminary Findings Report (v0)

```yaml
retrieval_header_version: 1
artifact_role: downstream-facing findings report (PRELIMINARY; safe to build on, one ceiling pending)
scope: >
  Actionable synthesis of the IG R-probe for the lanes that consume it (monitoring policy +
  capture/projection-store). States the operating guidance NOW so downstream work can progress on
  preliminary findings, marks what is measured vs pending, and points to the evidence record.
use_when:
  - A downstream lane needs the IG read-rate operating guidance before the full characterization lands.
  - Sizing monitoring cadences or the projection-store engine on current evidence.
authority_boundary: retrieval_only
open_next:
  - docs/product/source_capture_toolbox/ig_r_probe_results_v0.md   # the evidence record + caveats
  - docs/product/data_capture_spine/orca_creator_monitoring_policy_architecture_v0.md   # Consumer A
stale_if:
  - The endurance run lands (pins or revises the at-pace daily-volume ceiling).
  - A later results/report version supersedes this.
```

## Status
`PRELIMINARY — safe to build on.` One thing is still being measured: the **at-pace daily-volume
ceiling** (endurance run in flight). Everything below is observed (logged-out probe, n=1 onset +
disambiguation); not validation/readiness. Evidence + caveats: `ig_r_probe_results_v0.md`.

## Bottom line (build on this now)
**IG logged-out reads are PACE-limited, not volume-limited.** Operate at **~2.5–4s between reads,
never sub-2s bursts**, in bounded attended sessions. At that pace the probe read **≥176 requests/
session with zero walls**; the true at-pace ceiling is being measured (preliminary: no volume cap
seen yet). The throttle that a fast burst trips is a **soft, IP-wide login-redirect that decays in
minutes** — not a ban. **Neither proxies/IP-rotation nor a sessioned/logged-in runtime is
warranted**; pace discipline is the whole mitigation.

## For the monitoring-policy lane (Consumer A)
- Your realistic cadences (daily / 3-day / weekly per post, batched; Tier-C weekly heartbeat) are
  **far gentler than the wall-tripping pace** → safe. The only rule: when a batch fires, **space the
  reads ≥~2.5s**; don't blast a bucket back-to-back.
- Treat **R as effectively non-binding for realistic rosters** at proper pace (volume ceiling pending,
  but ≥176/session clean and likely much higher). Size Tier-A breadth on coverage need, not on a
  scarce read budget.
- **Virality sprints (6h/12h) are safe** — hours-spaced reads are orders of magnitude below the pace
  wall. (Carve-out (B) note: this de-risks the cadence; (B) itself is still lane-only, not on `main`.)

## For the capture / projection-store lane (Consumer B)
- **No high-volume or write-contention problem.** Reads are pace-limited (not volume-limited), and
  the projection is a low-frequency batch derivation → **supports the storage backbone's
  throughput-bounded / no-server engine pick.** R does not gate the engine upward.
- **Per-platform read cost (IG):** ≈ **16 modeled IG-requests per full creator read** (1 profile ≈ 4
  + up to 12 items), **~89% call-yield** (image-carousel posts can miss the `og:description` signal —
  a content-shape gap, not a block). Volume estimate = `M creators × ~16 req × cadence`.
- **Do NOT couple capture to the probe:** the probe writes no `metric_observations`; the IG producer
  slice (PR #158 typed-capture) owns that wiring.

## Measured vs pending
| Finding | State |
|---|---|
| Limit is pace, not volume | **Measured** (run1 176 clean @≥2s vs run2 wall @sub-2s) |
| Safe pace ~2.5–4s | **Adopted** (owner) — margin above the ~2s trip |
| Onset = soft, IP-wide, login-redirect, decays | **Measured** (disambiguation: 2 creators walled, 1 recovered) |
| Neither proxies nor sessions | **Decided** |
| Burst (6h/12h) safe | **Inferred** (run waived — owner: safe) |
| At-pace daily-volume ceiling | **PENDING** (endurance run in flight) |
| Exact pace threshold (1s? burst-shape?) | Deferred (perma-block contingency) |

## Non-claims
Preliminary synthesis from logged-out attended probe runs (raw in gitignored `_test_runs/`), n=1
onset. "Safe"/"clean" describe observed probe behavior at the tested pace/volume, not a guarantee.
Not validation, readiness, buyer-proof, or commercial authorization.
