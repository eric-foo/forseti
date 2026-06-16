# IG Capture Rate — Preliminary Findings Report (v0)

```yaml
retrieval_header_version: 1
artifact_role: downstream-facing findings report (PRELIMINARY; usable for bounded planning, one ceiling pending)
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
  - A later endurance run pins or revises the at-pace daily-volume ceiling.
  - A later results/report version supersedes this.
```

## Status
`PRELIMINARY — usable for bounded planning, not a build-go.` One thing remains unmeasured: the **at-pace daily-volume
ceiling**. The first endurance attempt aborted `ip_not_recovered`; a later retry wrote only
`endurance_log.jsonl`, never got two clean warm-up reads, and wrote no `endurance_summary.json`.
Everything below is observed (logged-out probe, n=1 onset + disambiguation + recovery-gated
attempt logs); not validation/readiness. Evidence + caveats: `ig_r_probe_results_v0.md`.

## Bottom line (bounded planning guidance)
**IG logged-out reads are PACE-limited, not volume-limited.** Operate at **~2.5–4s between reads,
never sub-2s bursts**, in bounded attended sessions. At that pace the probe read **≥176 requests/
session with zero walls**; the true at-pace ceiling remains unmeasured (preliminary: no volume cap
seen before the sub-2s wall). The throttle that a fast burst trips is a **soft, IP-wide
login-redirect that is STICKY once tripped** — it persisted **≥12 min** under gentle periodic
probing, and a later retry still failed to clear two warm-up reads over ~21.6 min; full recovery
needs a longer **fully-quiet** cooldown (>21 min, unmeasured) — not a ban. **Neither proxies/IP-rotation nor a sessioned/logged-in runtime is
warranted**; pace discipline is the whole mitigation.

## For the monitoring-policy lane (Consumer A)
- Your realistic cadences (daily / 3-day / weekly per post, batched; Tier-C weekly heartbeat) are
  **far gentler than the wall-tripping pace** → compatible with the current preliminary envelope. The only rule: when a batch fires, **space the
  reads ≥~2.5s**; don't blast a bucket back-to-back.
- Treat **R as effectively non-binding for realistic rosters** at proper pace (volume ceiling pending,
  but ≥176/session clean and no volume cap seen before the pace wall). Size Tier-A breadth on coverage need, not on a
  scarce read budget.
- **Virality sprint cadence is low-risk from the R-pace perspective** — hours-spaced reads are orders of magnitude below the pace
  wall. (Carve-out (B) note: this de-risks the cadence; (B) itself is still lane-only, not on `main`.)

## For the capture / projection-store lane (Consumer B)
- **No high-volume or write-contention problem.** Reads are pace-limited (not volume-limited), and
  the projection is a low-frequency batch derivation → **supports the storage backbone's
  throughput-bounded / no-server engine pick.** R does not gate the engine upward.
- **Per-platform read cost (IG):** ≈ **16 modeled IG-requests per full creator read** (1 profile ≈ 4
  + up to 12 items), **~89% call-yield** (image-carousel posts can miss the `og:description` signal —
  a content-shape gap, not a block). Volume estimate = `M creators × ~16 req × cadence`.
- **Do NOT couple capture to the probe:** this R result is read-measurement evidence, not
  typed-capture acceptance. Current packet-mode runner surfaces may write metric observations, but the
  R-probe conclusion must not be used as proof that the producer/projection path is accepted.

## Measured vs pending
| Finding | State |
|---|---|
| Limit is pace, not volume | **Measured** (run1 176 clean @≥2s vs run2 wall @sub-2s) |
| Safe pace ~2.5–4s | **Adopted** (owner) — margin above the ~2s trip |
| Onset = soft, IP-wide, login-redirect; **sticky ≥12 min** | **Measured** (disambig + endurance warm-up: persisted ≥12 min under probing; occasional 1-read slip-through; retry 2 still not both-clean through ~21.6 min) |
| Neither proxies nor sessions | **Decided** |
| Burst (6h/12h) cadence posture | **Inferred** (run waived — owner treated cadence as de-risked; lane authorization remains separate) |
| At-pace daily-volume ceiling | **STILL PENDING** — endurance attempt aborted (`ip_not_recovered`); retry 2 has log-only warm-up failure and no summary; needs a long fully-quiet cooldown first |
| Exact pace threshold (1s? burst-shape?) | Deferred (perma-block contingency) |

## Non-claims
Preliminary synthesis from logged-out attended probe runs (raw in gitignored `_test_runs/`), n=1
onset; retry 2 is log-only because the expected summary file is absent. "Safe"/"clean" describe
observed probe behavior at the tested pace/volume, not a guarantee.
Not validation, readiness, buyer-proof, or commercial authorization.
