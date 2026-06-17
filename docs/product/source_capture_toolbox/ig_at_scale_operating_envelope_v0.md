# IG At-Scale Operating Envelope (v0)

```yaml
retrieval_header_version: 1
artifact_role: Product artifact — IG at-scale capture operating-envelope recommendation (non-authorizing)
scope: >
  Sizes the beauty-vertical IG capture operating envelope from the current per-IP, pace-bound R
  evidence: proxy cost/benefit as a fallback, human-like cadence/scroll posture beyond bounded_jitter,
  the ideal operating-account/IP count, and the owner-selected two-lane serious-v0 path for
  1,000 beauty creators. Does not authorize live capture, proxy purchase, session/cookie wiring,
  scheduler/runtime work, network configuration, or commercial-scale collection.
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
  - A later route probe revises the current local egress cooldown/recovery posture, or the measured
    `768x1024` profile-enumeration viewport no longer exposes DOM permalinks.
  - Proxy provider pricing or acceptable-use posture materially changes.
  - IG moves the public signal behind auth, changes the block mode, or changes the logged-out read substrate.
```

## Status

`OPERATING_ENVELOPE_V0 — preliminary, costed fallback; not authorization.` This uses the current
R-probe evidence, a 2026-06-16 proxy-pricing spot check, and the 2026-06-16 branch-lane closeout
for the second-egress operating posture. It is not validation, readiness, commercial authorization,
a live-run instruction, a proxy-purchase approval, a network-setup instruction, or a runner build spec.

## Source basis

Local sources reread on current `origin/main` (`73b091bc`, 2026-06-16):

- `docs/decisions/wind_caller_calibration_carveout_v0.md`
- `docs/product/source_capture_toolbox/ig_r_probe_results_v0.md`
- `docs/product/source_capture_toolbox/ig_capture_rate_findings_report_v0.md`
- `docs/product/source_capture_toolbox/ig_sustained_cadence_r_probe_design_v0.md`
- `docs/product/data_capture_spine/orca_creator_monitoring_policy_architecture_v0.md`
- `docs/product/source_capture_toolbox/ig_capture_findings_consolidated_v0.md`
- `orca-harness/runners/run_source_capture_ig_calls_packet.py`

Successor-lane live addendum (2026-06-17; gitignored receipts, no proxy endpoint/exit-IP/session
secret recorded in durable docs):

- Current local egress + logged-out can soft-wall (`web_profile_info` 401 / login redirect).
- Residential rotating proxy + logged-out returned `web_profile_info` 200; vanilla Playwright was
  sufficient for that API result, so CloakBrowser was not the differentiator in this probe.
- Owner-created session state on current egress returned `web_profile_info` 200. This is a fallback
  candidate, not a default runtime recommendation.
- Current local egress + logged-out recovered after an hours-long quiet window in a bounded smoke:
  `@hyram`, no proxy, no session, `768x1024`, max 4 items, 8-12s gaps, 4/4 call slices captured,
  2 posts + 2 reels, 2 observed reel `view_count` values, no packet warnings. The first sandboxed
  attempt failed before source access because Playwright subprocess startup was denied by the local
  execution environment; the re-run outside that sandbox wrote the packet.
- A later current-egress logged-out Stage 1 slice also completed without block signals:
  gitignored raw root
  `orca-harness/_test_runs/ig_stage1_current_egress_logged_out_768x1024_max12_20260617_162730/`;
  five prior repo-named handles (`hyram`, `nikkietutorials`, `kayla.ryan1`, `theglownarrative`,
  `milkydew_`), no proxy, no session, `768x1024`, max 12 items/handle, configured 8-12s item gaps
  and 30s inter-profile gaps; 5/5 packets wrote, 60 items enumerated, 52 full call-signal captures,
  8 `partial_signal` content-shape misses, 45 observed `view_count` values, no packet warnings, and
  no `access_blocked`, `capture_failed`, or `no_signal` item statuses. This is Stage 1 slice
  evidence only, not repeated-window sustainability.
- Profile DOM permalink extraction is viewport-sensitive: `768x1024` and `1280x1200` returned 12
  grid permalinks; `1280x720`, `820x1180`, and `1024x1366` returned none in the same bounded route.

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

Do **not** pre-buy proxies or add IG accounts as the default architecture for the current
beauty-vertical IG monitoring posture.

The durable live constraint remains per-egress-IP **pace**, not account count and not ordinary
session volume. The 2026-06-17 successor probes add a route-selection caution: the current local
egress can be logged-out soft-walled, but later recovered after an hours-long quiet window for one
bounded logged-out smoke and then completed one five-handle Stage 1 slice without block markers; an
alternate residential egress worked logged-out, and own-session current egress worked for
`web_profile_info`. Operate logged-out egress paths at bounded human-paced spacing, in bounded,
human-initiated/self-terminating sessions. For the owner-selected
**1,000 creator serious v0**, the smallest reliable operating path is still:

- **Lane 1:** main laptop on home fibre/home internet.
- **Lane 2:** second laptop on phone USB tether or other mobile-data upstream.
- **Do not use a VM for the two-lane setup.** A separate physical laptop plus mobile-data egress is
  cleaner. Defer VM use until a third distinct egress lane is actually needed.
- **Do not treat a second laptop on the same home Wi-Fi/fibre as lane 2.** It is the same public egress.
- **Do not rotate per request.** Assign creators/due buckets to stable lanes.

If Lane 1 re-walls or remains logged-out soft-walled after a fully quiet cooldown, do not conclude
that IG is globally inaccessible. Treat it as an egress-route problem: prefer the mobile-data lane
or another clean logged-out egress before normalizing a paid proxy or account/session runtime.

The ideal operating-account count for the current logged-out path is therefore:

- **Small/default exploratory posture:** 1 operating context / egress path; no logged-in/session
  account used.
- **Current serious-v0 posture:** 2 distinct logged-out egress lanes for the 1,000 creator plan,
  only after non-IG isolation checks confirm different public IP/provider paths.
- **Fallback expansion:** a third distinct egress lane only if measured demand cannot fit the
  two-lane window or repeated compliant-pace blocks persist after fully quiet cooldown.
- **Ceiling discipline:** stay within the carve-out's start-<=5, cap-<=10 operating-account ceiling;
  never run multiple accounts on one egress and count that as throughput.

## 1,000-Creator Serious-v0 Working Envelope

Use observed rate and target rate separately:

| Basis | Per lane | Two lanes | 3,500 modeled requests/day |
| --- | ---: | ---: | ---: |
| Observed clean run | ~285 modeled requests/hour/IP | ~570/hour aggregate | ~6.1 aggregate hours |
| Next target to test | ~400 modeled requests/hour/IP at ~9s/request | ~800/hour aggregate | ~4.4 aggregate hours |

The 9s/request figure is a planning target, not a validated safe rate. The observed clean evidence
remains ~176 modeled requests over 37 minutes, or about 285 modeled requests/hour/IP. Use the
two-lane plan to make the daily window comfortable, not to justify sub-2s behavior or evasion.

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
| 1,000 serious-v0 IG plan | ~2,800-3,500 modeled IG-requests/day | ~82-103 GB/month | ~$287-$721/month |

If actual browser transfer averages 5 MB/request, multiply those dollar ranges by 5. This still makes
proxy spend a fallback operating cost, not the current bottleneck: the current bottleneck is avoiding
the sub-2s pace wall and recovering cleanly after a wall.

## Human-Like Cadence / Scroll Model

The runner's `bounded_jitter` is necessary but too thin as an operating model. The envelope should
shape whole sessions, not only item-to-item sleeps.

Default session posture:

- Human-initiated, bounded, self-terminating session; no standing crawler.
- Due-list only for passive monitoring; no discovery during passive sessions.
- One egress path for exploratory/default work; two stable egress lanes for the current 1,000 creator
  serious-v0 plan after non-IG isolation checks pass.
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
| Exploratory/default logged-out monitoring | 1 egress path; no session account | R is per IP; extra accounts on one IP add zero throughput. |
| Current 1,000 creator serious-v0 path | 2 distinct egress paths; no session accounts | Keeps the daily monitoring window operationally comfortable without accounts, proxies, or VM complexity. |
| First fallback after two-lane measured compliant-pace blocks | 3 distinct egress paths | Tests whether capacity is additive without burning the <=5 starting envelope. |
| Larger fallback if one-IP session windows cannot fit roster demand | `ceil(demand / observed_per_ip_R)` distinct egress paths, capped by owner posture | Add IPs only from measured demand; do not pre-buy capacity. |
| Session/account runtime | 0 by default; separately authorized fallback/probe only | Own-session current egress worked for `web_profile_info`, but sustained cadence/account risk is unmeasured and should not replace clean logged-out egress by default. |

Do not use the full <=10 cap as a target. It is a ceiling for risk control, not an operating goal.
The right number is the smallest number of distinct egress paths that keeps compliant-pace sessions
inside the intended monitoring window.

## Lane-2 Setup Decision

The current lane-2 operating decision is:

```text
lane_1 = main_laptop + home_fibre
lane_2 = second_laptop + phone_usb_tether_or_mobile_data
vm = deferred_until_third_distinct_egress_needed
```

Before any future IG work, run only non-IG isolation checks:

1. Compare public IP/provider on both laptops using a plain IP checker.
2. Confirm the second laptop loses internet when the phone tether/mobile upstream is disconnected.
3. Confirm the second laptop does not silently rejoin home Wi-Fi.
4. Confirm the phone is on mobile data, not home Wi-Fi.

Passing these checks would prove only network separation, not IG safety, readiness, validation,
or authorization to capture.

## Open Measurements

- At-pace daily-volume ceiling remains unmeasured. The second endurance retry wrote only warm-up log
  rows and no summary.
- Current local egress logged-out recovery has progressed from one max-4 `@hyram` smoke to one
  five-handle Stage 1 slice; repeated-window sustainability, exact cooldown length, two-lane
  additivity, and daily ceiling remain unmeasured.
- Profile-enumeration viewport behavior remains first-measured but stronger: `768x1024` exposed 12
  DOM item links across the five-handle Stage 1 slice. It is still not a permanent IG guarantee.
- Exact pace threshold remains unpinned; known safe/unsafe shape is >=~2s clean in run 1 and sub-2s
  wall in run 2.
- Throttle decay time remains unpinned; evidence says longer than the prior "minutes" assumption and
  not cleared by the retry pattern.
- Average bytes per IG-request equivalent is unmeasured; needed for proxy cost precision.
- Configured 8-12s item gaps have completed in one Stage 1 slice; a true end-to-end 9s/request
  operating rate is not separately modeled or validated.
- The second-laptop/mobile-data lane has not been isolation-tested in this repo lane.

## Non-Claims

Not validation, readiness, buyer proof, legal advice, commercial authorization, proxy-purchase
approval, network-setup approval, session/cookie authorization, anti-detect implementation, CAPTCHA
solving, scheduler runtime, production deployment, ECR, Cleaning, Judgment, or projection acceptance.
Price examples are a dated spot check only; verify provider pages and acceptable-use terms before
any spend.
