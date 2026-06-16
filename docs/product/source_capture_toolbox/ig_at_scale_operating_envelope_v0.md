# IG At-Scale Operating Envelope (v0)

```yaml
retrieval_header_version: 1
artifact_role: Product artifact — IG at-scale capture operating-envelope recommendation (non-authorizing)
scope: >
  Sizes the beauty-vertical IG capture operating envelope from the current per-IP, pace-bound R
  evidence: proxy cost/benefit as a fallback, human-like cadence/scroll posture beyond bounded_jitter,
  and the ideal operating-account/IP count. Does not authorize live capture, proxy purchase,
  session/cookie wiring, scheduler/runtime work, or commercial-scale collection.
use_when:
  - Deciding whether the current beauty-vertical IG capture lane needs proxies, more operating accounts, or only pace discipline.
  - Translating the IG R-probe result into bounded monitoring-session defaults.
  - Checking the fallback trigger for adding egress IPs if persistent blocks appear.
authority_boundary: retrieval_only
open_next:
  - docs/product/source_capture_toolbox/ig_r_probe_results_v0.md
  - docs/product/source_capture_toolbox/ig_capture_rate_findings_report_v0.md
  - docs/decisions/wind_caller_calibration_carveout_v0.md
  - docs/product/data_capture_spine/orca_creator_monitoring_policy_architecture_v0.md
stale_if:
  - A fuller R run pins the at-pace daily-volume ceiling, exact pace threshold, or throttle decay time.
  - The carve-out is amended to authorize sessions, auto-sprints, commercial scale, or a different account cap.
  - Proxy provider pricing or acceptable-use posture materially changes.
  - IG moves the public signal behind auth, changes the block mode, or changes the logged-out read substrate.
```

## Status

`OPERATING_ENVELOPE_V0 — preliminary, costed fallback; not authorization.` This uses the current
R-probe evidence and a 2026-06-16 proxy-pricing spot check. It is not validation, readiness,
commercial authorization, a live-run instruction, a proxy-purchase approval, or a runner build spec.

## Source basis

Local sources reread on current `origin/main` (`73b091bc`, 2026-06-16):

- `docs/decisions/wind_caller_calibration_carveout_v0.md`
- `docs/product/source_capture_toolbox/ig_r_probe_results_v0.md`
- `docs/product/source_capture_toolbox/ig_capture_rate_findings_report_v0.md`
- `docs/product/source_capture_toolbox/ig_sustained_cadence_r_probe_design_v0.md`
- `docs/product/data_capture_spine/orca_creator_monitoring_policy_architecture_v0.md`
- `docs/product/source_capture_toolbox/ig_capture_findings_consolidated_v0.md`
- `orca-harness/runners/run_source_capture_ig_calls_packet.py`

External pricing spot-check (current enough for a v0 estimate; verify before spend):

- IPRoyal official residential proxy pricing page, opened 2026-06-16:
  `https://iproyal.com/pricing/residential-proxies/`
- TechRadar 2026 proxy-provider survey, opened 2026-06-16:
  `https://www.techradar.com/best/proxy`
- TechRadar provider reviews for Bright Data, Oxylabs, and Decodo, opened 2026-06-16:
  `https://www.techradar.com/reviews/bright-data`,
  `https://www.techradar.com/reviews/oxylabs`,
  `https://www.techradar.com/reviews/smartproxy`

## Bottom line

Do **not** buy proxies or add accounts for the current beauty-vertical IG monitoring posture.

The live constraint is per-egress-IP **pace**, not account count and not ordinary session volume.
Operate one logged-out egress path at the owner-adopted 2.5-4s minimum spacing, in bounded,
human-initiated/self-terminating sessions. Add proxy/IP capacity only after a measured trigger:
repeated blocks at compliant pace after a long fully-quiet cooldown, or a roster/cadence demand that
cannot fit into acceptable bounded sessions on one egress.

The ideal operating-account count for the current logged-out path is therefore:

- **Current default:** 1 operating context / egress path; no logged-in/session account used.
- **Fallback start:** 2 distinct `(operating context, egress IP)` pairs only after the trigger above.
- **Ceiling discipline:** stay within the carve-out's start-<=5, cap-<=10 operating-account ceiling;
  never run multiple accounts on one egress and count that as throughput.

## Proxy Cost / Benefit

### What proxies buy

Proxies buy additional egress IPs. They do **not** buy permission to read sub-2s, bypass the
carve-out, run a standing crawler, wire sessions/cookies, or ignore cooldowns. Each added IP must run
the same pace-safe cadence as the baseline IP.

Use this trigger:

```text
add_proxy_if:
  compliant_pace_block_repeats_after_quiet_cooldown: yes
  OR bounded_session_window_cannot_fit_roster_demand_on_one_egress: yes
else:
  no_proxy_spend
```

### Cost model

Most relevant residential/mobile proxy products are bandwidth-priced. Current small-plan residential
spot-checks cluster around roughly **$3.50-$7/GB**; bulk enterprise can be lower but usually requires
large monthly commitments. Examples from the 2026-06-16 spot check:

| Source | Observed pricing signal | Use in this lane |
| --- | --- | --- |
| IPRoyal official page | Residential PAYG examples around $7.35/GB for 1 GB and $5.15/GB for 50 GB; nav also advertises residential "from $1.75/GB" | small-fallback upper bound |
| TechRadar 2026 proxy survey | Decodo residential PAYG reported at $3.50/GB; enterprise example $1.50/GB at 1000 GB/month | realistic low/mid market bound |
| TechRadar Bright Data review/survey | Bright Data residential PAYG reported around $4-$5.04/GB; monthly plans lower per GB with large minimums | premium provider bound |
| TechRadar Oxylabs review | Oxylabs residential PAYG reported around $4/GB; enterprise tiers down to ~$2/GB at high volume | premium/bulk bound |

Use the formula, not a fixed price:

```text
monthly_proxy_cost ~= GB_per_month * price_per_GB
GB_per_month ~= (modeled_IG_requests_per_month * average_transfer_MB_per_request) / 1024
```

The current R-probe measured request equivalents, not bytes. Until a byte-measurement run exists,
treat proxy cost as a sensitivity:

| Roster envelope | Policy demand basis | At 1 MB/request | At $3.50-$7/GB |
| --- | --- | --- | --- |
| M=200 illustrative vertical | ~308 modeled IG-requests/day | ~9 GB/month | ~$32-$65/month |
| M=1000 illustrative vertical | ~1540 modeled IG-requests/day | ~46 GB/month | ~$160-$323/month |

If actual browser transfer averages 5 MB/request, multiply those dollar ranges by 5. This still makes
proxy spend a fallback operating cost, not the current bottleneck: the current bottleneck is avoiding
the sub-2s pace wall and recovering cleanly after a wall.

## Human-Like Cadence / Scroll Model

The runner's `bounded_jitter` is necessary but too thin as an operating model. The envelope should
shape whole sessions, not only item-to-item sleeps.

Default session posture:

- Human-initiated, bounded, self-terminating session; no standing crawler.
- Due-list only for passive monitoring; no discovery during passive sessions.
- One egress path by default; no concurrent multi-egress run unless the fallback trigger is met.
- Hard floor: never sub-2s; operating target: 2.5-4s minimum spacing with longer natural gaps.
- Abort on any login redirect, 429-like interstitial, or network-security block; then fully quiet,
  not periodic probing.

Cadence shape beyond bounded_jitter:

- Start with a short warm-up: one low-density profile read, then continue only if clean.
- Batch by due bucket, not by "blast every creator"; keep reads attributable to a bounded monitoring
  reason.
- Insert idle gaps after small clusters: e.g. a handful of creator/item reads, then a longer pause.
- Vary profile scroll depth within the bounded cap; do not turn profile scroll into deep discovery.
- Avoid tight same-handle loops unless the run is explicitly a bounded hot-post check.
- Keep per-run item caps; full-history backfill remains out of scope.
- Record block outcome and stop reason visibly; do not create fake success packets.

Daypart posture:

- Prefer a few owner-started windows over continuous execution.
- Virality sprint behavior remains constrained by the current carve-out state. Until the durable
  carve-out and runtime build both authorize auto-launch behavior, treat tight 6h/12h checks as
  attended/operator-initiated or best-effort within-session only.

## Account / IP Count

The account count question should be answered as egress math, not social-account math.

| Scenario | Ideal count | Reason |
| --- | --- | --- |
| Current logged-out monitoring | 1 egress path; no session account | R is per IP; extra accounts on one IP add zero throughput. |
| First fallback after measured compliant-pace blocks | 2 distinct egress paths | Tests whether capacity is additive without burning the <=5 starting envelope. |
| Larger fallback if one-IP session windows cannot fit roster demand | `ceil(demand / observed_per_ip_R)` distinct egress paths, capped by owner posture | Add IPs only from measured demand; do not pre-buy capacity. |
| Session/account runtime | 0, unless owner amends carve-out | Current lane forbids cookies/sessions in committed runner paths. |

Do not use the full <=10 cap as a target. It is a ceiling for risk control, not an operating goal.
The right number is the smallest number of distinct egress paths that keeps compliant-pace sessions
inside the intended monitoring window.

## Open Measurements

- At-pace daily-volume ceiling remains unmeasured. The second endurance retry wrote only warm-up log
  rows and no summary.
- Exact pace threshold remains unpinned; known safe/unsafe shape is >=~2s clean in run 1 and sub-2s
  wall in run 2.
- Throttle decay time remains unpinned; evidence says longer than the prior "minutes" assumption and
  not cleared by the retry pattern.
- Average bytes per IG-request equivalent is unmeasured; needed for proxy cost precision.

## Non-Claims

Not validation, readiness, buyer proof, legal advice, commercial authorization, proxy-purchase
approval, session/cookie authorization, anti-detect implementation, CAPTCHA solving, scheduler
runtime, production deployment, ECR, Cleaning, Judgment, or projection acceptance. Price examples are
a dated spot check only; verify provider pages and acceptable-use terms before any spend.
