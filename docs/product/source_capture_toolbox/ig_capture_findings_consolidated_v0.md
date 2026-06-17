```yaml
retrieval_header_version: 1
artifact_role: consolidated capture findings (non-authorizing)
scope: >
  Single consolidated statement of what is currently known about capturing the IG
  (Instagram) wind-caller / creator-momentum signal — calls, profile stats, and
  reel/video view counts — across the per-source recons and the shipped
  calls-capture build. Supersedes scattered per-doc claims where they conflict,
  and records the corrections made along the way. Non-authorizing: a findings
  consolidation, not a build go, validation, or commercial authorization.
use_when:
  - Onboarding the IG capture path or checking the current best understanding before re-probing.
  - Scoping the reel-view-count build or the H5 sustained-cadence probe.
  - Resolving an apparent conflict between older IG recon docs (this note is the current consolidation).
authority_boundary: retrieval_only
open_next:
  - docs/product/source_capture_toolbox/ig_creator_discovery_spec_v0.md
  - docs/product/source_capture_toolbox/ig_reel_viewcount_capture_feasibility_recon_v0.md
  - docs/product/source_capture_toolbox/ig_wind_caller_capture_feasibility_recon_v0.md
  - docs/product/source_capture_toolbox/ig_wind_caller_calls_capture_build_architecture_v0.md
  - docs/product/source_capture_toolbox/capture_recon_index_v0.md
  - docs/decisions/wind_caller_calibration_carveout_v0.md
stale_if:
  - IG moves any signal behind auth, changes og:description shape, the profile-feed payload, or the grid doc_id.
  - IG changes the profile DOM responsive variant such that the measured profile-enumeration
    viewport(s) no longer expose post/reel permalinks.
  - A fuller H5/R run pins the at-pace ceiling, exact pace threshold, or throttle decay time.
  - The reel-view-count build ships (moves that signal from feasibility-proven to built).
status: CONSOLIDATED — calls+stats SHIPPED logged-out; reel view-count FEASIBILITY-PROVEN logged-out; route/viewport addendum 2026-06-17; scale first-measured, with at-pace ceiling still open
```

# Instagram Capture Findings — Consolidated (v0)

## Headline

**The IG wind-caller signal — public "calls" (captions + engagement), profile stats, and
reel/video view counts — remains capturable by a headless browser, and the first-class product
route is still logged-out on a clean/working public egress.** The 2026-06-17 live probes refine the
older absolute wording: current local egress can be logged-out soft-walled
(`web_profile_info` 401 / login redirect), but later recovered after an hours-long quiet window for
one bounded logged-out `@hyram` max-4 smoke capture. A residential proxy route returned logged-out
`web_profile_info` 200 and profile-grid permalinks at measured viewport(s). Owner-created session
state on current egress also returned `web_profile_info` 200, so an own-session route is technically
viable as a fallback/probe candidate, but it is not the default product path and its account risk and
sustained cadence remain unmeasured.

## Signal-by-signal

| Signal | Where it lives | Auth | Status | Source |
| --- | --- | --- | --- | --- |
| **Calls** — verbatim caption + likes + comments + date + `#ad` flag, per post/reel | post/reel page **`og:description`** meta | **logged-out route** | **BUILT + prior validated** (runner; 832 tests pass; live `@hyram` 6/6); 2026-06-17 probes found profile-enumeration viewport fragility | calls recon + build arch; `run_source_capture_ig_calls_packet.py` (merged); 2026-06-17 route/viewport addendum |
| **Profile stats** — followers / following / post counts (snapshot) | profile **`og:description`** + `web_profile_info` JSON | **logged-out** | capturable now; **historical series** = Social Blade (free, recent window) or self-logging over time | calls recon + build arch |
| **Reel / video view counts** — `video_view_count` per media | **profile-feed JSON** (`web_profile_info` + grid `graphql/query`), follow `end_cursor` for depth | **logged-out** | **FEASIBILITY-PROVEN** (deep: 25 pages, 365 media back to 2017, no wall/`429`); **build deferred** | reel-viewcount recon (this lane) |
| **Media / video bytes** | n/a | — | **OUT of scope** — never probed; not captured | — |

## Auth / route posture (the load-bearing conclusion)

- **Calls + stats**: the runner was built `logged-out` by construction — *"needs no session"*; non-claims
  include *"not login or session capture"*, *"not proxy or session injection"* for that shipped path.
- **Reel view counts**: the profile-feed JSON (`web_profile_info`, **200 cookieless** in a browser
  context) and the grid `graphql/query` cursor pagination both return `video_view_count`
  logged-out; a session run was **byte-identical** to logged-out.
- **2026-06-17 route refinement**: current local egress logged-out can soft-wall, but one later
  smoke-level logged-out run after an hours-long quiet window captured `@hyram` 4/4 with no packet
  warnings; logged-out alternate egress worked and own-session current egress worked for
  `web_profile_info`. Therefore, do not make sessions the default or use them to reach
  private/auth-gated material; treat own-session current-egress capture as a separately authorized
  fallback/probe lane only if clean logged-out egress/mobile/proxy paths are too costly or
  unavailable.
- **Therefore**: keep the IG runner logged-out-first. Re-open session/runtime wiring only as an
  explicit fallback decision after measured logged-out route/cadence evidence, because the sustained
  account/session risk is not characterized here.

## Method map (where each signal lives, how to get it)

- **Calls + snapshot stats** → parse the post/reel/profile **`og:description`** meta from a
  headless logged-out browser snapshot. Enumerate items from the profile grid when the responsive
  variant exposes `/p/` and `/reel/` permalinks; the measured candidate viewport is `768x1024`.
- **Profile item enumeration** → profile DOM links are viewport-sensitive, not simply absent:
  `1280x720`, `820x1180`, and `1024x1366` produced no DOM item links in the 2026-06-17 proxy route,
  while `768x1024` and `1280x1200` each produced 12. If DOM links are absent at one viewport, use
  `web_profile_info` / profile-feed JSON shortcodes as fallback evidence before calling NO-GO.
- **Reel view counts** → capture the **profile-feed response bodies** during enumeration
  (`web_profile_info` first page) and **follow the grid `end_cursor`** via `graphql/query`
  (`doc_id=7950326061742207`, `id`=user_id) for depth; parse `video_view_count` per `shortcode`.
- **Deep history** → cursor pagination, not UI scroll (see Corrections #3).

## Corrections log (claims overturned by measurement)

1. **"`web_profile_info` is 429 cookieless → needs login"** → **WRONG/imprecise.** It returns
   **200 cookieless** in a real browser context (with IG's `X-IG-App-ID`/web headers). The 429
   was the header-less `direct_http` rung, not a browser XHR.
2. **"Calls capture is attended, logged-in"** (original recon framing) → **corrected to
   logged-out** by the build probe; the shipped runner is logged-out.
3. **"Reel view-count depth walls early logged-out"** → **WRONG; a measurement artifact.** A
   UI-scroll probe with a DOM login-heuristic false-walled on pass 1 (the heuristic fired
   regardless of auth; `mouse.wheel` never triggered IG's infinite-scroll — identical
   logged-out/session results were the tell). Following the grid's own `end_cursor` showed deep,
   unwalled logged-out pagination. (Capture-recon **Pattern 1**: *"blocked/limited" is a
   hypothesis — use the right mechanism before recording a NO-GO.*)
4. **"Rendered-grid permalink extraction is impossible; only JSON works"** → **WRONG.** A saved
   `1280x720` profile DOM contained no `/p/` or `/reel/` hrefs and no shortcodes, but logged-out
   proxy probes at `768x1024` and `1280x1200` produced 12 rendered profile-grid permalinks with no
   extra settle/scroll. The correct finding is viewport/layout sensitivity, with JSON as the backup
   enumerator.

## Build status

- **Calls capture: SHIPPED** — logged-out runner, parsers, scroll enumeration, cadence, packet
  writer; full suite passes; live-verified. Merged.
- **Calls runner robustness: PARTIAL PATCHED** — `run_source_capture_ig_calls_packet.py` now defaults
  profile/item captures to the measured `768x1024` viewport, reducing the known false-empty DOM grid
  failure at `1280x720`; it also exposes proxy use as an explicit label-indirected runner option
  (`--proxy-label`, with category read from the registered sidecar by default) and records only proxy
  category provenance. A bounded 2026-06-17 proxy smoke run against `@hyram` captured 4/4 call slices
  and `web_profile_info` + grid JSON returned 200. The runner can still hard-stop when DOM permalink
  enumeration is empty before using profile-feed JSON, so JSON shortcode fallback remains a separate
  patch candidate.
- **IG projection transformer/helper: PROTOTYPE PATCHED** — `source_capture/ig_projection.py` now
  builds a view-only mechanical row index from existing IG packet `metric_observations`, preserving
  packet/slice/file anchors, numeric-id identity when present, shortcode/content kind,
  value/posture coupling, and observed zero values. `run_ig_creator_momentum_projection.py` can
  materialize that view from an existing packet directory or manifest. This is a packet-derived
  photo-album/index step, not a scheduler, storage engine, production projection, momentum score, or at-scale validation.
- **Reel view-count capture: NOT built** — feasibility proven only. The build would extend the
  logged-out runner to capture profile-feed response bodies + follow the grid cursor, parsing
  `video_view_count` per `shortcode` onto the call slices. Needs the runner to **expose response
  bodies** and **follow the cursor**. **Separate, deferred, needs an explicit build go.**

## Residuals / not-proven

- **Sustained cadence at scale (H5)** — first measured, not fully characterized. The R-probe found
  the constraint is per-IP **pace**, not ordinary session volume: ≥176 modeled requests at ≥~2s
  spacing were clean, while a sub-2s burst tripped an IP-wide login redirect. Two recovery-gated
  endurance attempts failed before measuring the at-pace daily ceiling, so exact threshold, daily
  ceiling, and decay time remain open. Subject-creator roster is uncapped; the per-run account
  limit is on our own capture/operating accounts, not on the number of creators tracked. See
  `ig_r_probe_results_v0.md` for the evidence record and caveats.
- **Route/viewport evidence is still narrow.** The 2026-06-17 route probes were bounded, mostly
  `@hyram`, and used a residential rotating proxy plus current-egress/session diagnostics and one
  current-egress recovery smoke. They prove the failure mode, a working viewport candidate, and that
  current egress can recover to smoke-level logged-out capture after a long quiet window; they do not
  validate a production runner patch, mobile-data lane, sustained current-egress cadence, or sustained
  account/session route.
- **Proxy-backed packet evidence is smoke-level only.** The 2026-06-17 runner packet proves one
  `@hyram` logged-out proxy run can capture recent calls and profile-feed JSON through the patched
  runner. It is not sustained-cadence, mobile-data, account/session, or at-scale validation.
- **Reel view counts are cumulative-at-capture**, not a time series — momentum requires the
  repeated-over-time harvesting the carve-out authorizes.
- **Image posts** carry no `video_view_count`; some values are `0`.
- **Media/video bytes** are out of scope and unprobed.
- Probes are **n=1–2 accounts** feasibility GOs, not at-scale validations.

## Posture / carve-out

Governed by `docs/decisions/wind_caller_calibration_carveout_v0.md` as amended (carve-out
2026-06-15 amendment): own operating/capture accounts ≤10 ceiling (ops start ≤5) — this cap
counts OUR OWN capture accounts, not subject creators; subject-creator roster is **uncapped**
(all creators in the vertical). ~1-month recent window, no full-history backfill,
repeated-**attended** (not a scheduled crawler). Method: **ACTIVE** (discovery + capture
decisions) = attended (human-initiated); **PASSIVE** (monitoring already-flagged creators) =
human-initiated, time-bounded, self-terminating — not a perpetual or scheduled standing crawler.
10-year bounded retention + immediate takedown-on-request. Stats at commercial scale →
licensed/bought-data posture.
*(direction_change_propagation 2026-06-15: cap-redefinition per carve-out 2026-06-15 amendment —
≤10/start-5 ceiling counts own operating/capture accounts; subject roster uncapped;
active/passive method posture defined. "10-year bounded retention + immediate takedown-on-request"
and "commercial scale → licensed/bought-data posture" clauses preserved verbatim.)*

## Non-claims

A findings consolidation, not authorization, build spec, validation, readiness, acceptance, or
legal advice. "Shipped" refers to the calls runner's merged + validated state; "feasibility-proven"
is a recon GO, not a built or at-scale claim. Per-doc sources above remain the primary record.
```
