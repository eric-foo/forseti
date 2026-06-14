```yaml
retrieval_header_version: 1
artifact_role: capture recon finding (non-authorizing)
scope: >
  IG reel/video VIEW-COUNT capture-feasibility recon for the creator-momentum /
  wind-caller lane. Records whether a reel's play/view count is capturable, on
  which surface, and at which auth state (logged-out vs session). Probe-first,
  before any build. Complements the calls-capture recon (captions + engagement),
  which did not resolve the reel view-count residual.
use_when:
  - Deciding whether reel view/play counts need a session/auth path or are reachable logged-out.
  - Scoping a reel-view-count build (where the signal lives; per-reel vs profile-feed; folds into existing runner or not).
  - Settling the "session-vs-logged-out" question for IG momentum-outcome signal.
authority_boundary: retrieval_only
open_next:
  - docs/product/source_capture_toolbox/capture_recon_index_v0.md
  - docs/product/source_capture_toolbox/ig_wind_caller_capture_feasibility_recon_v0.md
  - docs/decisions/wind_caller_calibration_carveout_v0.md
stale_if:
  - IG changes the profile-feed payload shape (web_profile_info / grid graphql/query) or moves video_view_count behind auth.
  - A logged-out pagination-depth / sustained-cadence probe lands (would close this finding's two open residuals).
  - A session (Phase 2) comparison run lands (would settle session-vs-logged-out depth).
status: RECON_GO_ON_REACHABILITY__PARTIAL_ON_DEPTH_AND_SCALE
```

# IG Reel View-Count Capture-Feasibility Recon (v0)

## What this is — and is not

This is a **capture recon finding**: a real, bounded, disposable probe of whether a reel's
play/view count is capturable, on which surface, and at which auth state. It was run
**probe-first, before any build**, to resolve the open residual the calls-capture recon left
("reel view/play count — in GraphQL JSON, not page DOM").

It is **non-authorizing**: not validation, readiness, buyer proof, or a build authorization.
It records what a single logged-out probe observed and, equally, what it did **not** test.
Raw capture lives only in gitignored `orca-harness/_test_runs/` (not retained here); the probe
script is a disposable, uncommitted `orca-harness/_scratch/` throwaway.

## Verdict (headline)

**GO on signal-reachability (logged-out) · PARTIAL on operational sufficiency.**

- The play/view count **is** capturable **logged-out** — `video_view_count`, per media node,
  keyed by `shortcode` — but it lives on the **profile feed payload**, **not** the reel
  permalink page. No session, cookies, or auth were used.
- It is **not** yet proven that logged-out reaches **enough depth** (before IG's login wall) or
  **sustains cadence at scale**. Those two legs are **untested** and are what decide whether
  logged-out alone suffices or a session path is warranted.

Consequence: the count rides the **same logged-out profile load** the calls-capture already
performs to enumerate the grid — so a build **folds into the existing logged-out runner**
(profile-feed response parse), **not** a per-reel capture and **not** a session-based runner —
*contingent on the depth/scale residuals closing*.

## The probe (what actually ran)

- **When / target:** 2026-06-14, `@hyram` (US skincare creator; feasibility probe subject, not
  a chosen calibration account), 3 recent reels: `DF3CdyJv79A`, `DEntAFPpiCv`, `DCM8psIJXl0`.
- **How:** one disposable Playwright (chromium, headless) run, **logged-out** (no
  `storage_state`). Exhaustive capture by design so a miss would be trustworthy: all network
  response bodies across the load lifecycle, full rendered HTML, and the `/embed/captioned/`
  endpoint — searched for five count-key variants (`play_count`, `view_count`,
  `video_view_count`, `ig_play_count`, `video_play_count`), plain and escaped.
- **Surfaces tested per reel:** A = embedded HTML JSON on the reel page; B = network
  XHR/GraphQL fired by the reel page; C = the public embed endpoint.

## Where the signal lives (and where it does not)

- **Reel permalink page (`/reel/<code>/`): NO count, logged-out.** A/B/C all returned zero hits
  for all 3 reels. No login redirect, **no 429**. So the reel page itself does not carry its own
  view count to a logged-out browser. (Your "logged-out gives nothing" intuition was correct
  *about the reel page*.)
- **Profile feed payload: count present, logged-out, 200.** Loading the profile fired two
  responses that carry `video_view_count` per media node:
  - `GET /api/v1/users/web_profile_info/?username=hyram` → **200 cookieless** (browser context),
    ~30 media nodes with `video_view_count` (e.g. 3995, 26542, 52303, 86640, 105479).
  - the grid pagination `GET /graphql/query` (`doc_id=7950326061742207`) → **200**, next page,
    ~11 more `video_view_count` (e.g. 343490, 41860, 25516).
  - **All 3 target reel shortcodes appear** in the `web_profile_info` payload, each as a node
    carrying `video_view_count` — i.e. the count maps to specific reels by `shortcode`.
- 16 reels were enumerable from the profile grid logged-out in this single load.

## Correction to the prior IG recon

The calls-capture recon recorded `web_profile_info` as **"API 429 cookieless → 200 logged-in"**.
This probe **refines** that: in a real **browser context** (carrying IG's `X-IG-App-ID` and web
headers), `web_profile_info` returned **200 cookieless** and carried `video_view_count`. The
earlier 429 was the **header-less `direct_http` rung**, not a browser-context XHR — both can be
true. Net: the momentum-outcome signal is **not** behind an auth wall; it is behind a
**header/context** difference the existing browser runner already satisfies.

## What this changes

- **Session adds no new *field*, but is warranted for *depth*.** `video_view_count` is free
  logged-out, so session buys **zero added signal** — but the depth probe shows logged-out
  **walls early** (first batch only). So the session lane is **not** dropped: it is justified
  for **depth/reliability** past the wall, not for the signal itself. Its scope is depth, not
  fields — which bounds the lock-in.
- **The "per-reel response-sniff hook" framing was wrong.** The count is a **profile-feed**
  artifact, not a reel-page one — so the build is *parse the profile-feed responses already
  loaded during grid enumeration*, attach `video_view_count` to the call slices by `shortcode`.
- **The momentum-grade question resolves in the good direction:** the dataset *can* be
  momentum-grade without session — *if* logged-out depth covers the target window.

## Open residuals (the two legs not tested — load-bearing)

1. **Logged-out pagination depth / login wall — TESTED: shallow, walls early.** A logged-out
   deep-scroll probe (2026-06-14, `@hyram`, up to 25 passes) hit the **login wall on the first
   scroll pass**, corroborated independently by a deeper feed/highlight pagination query
   (`doc_id=18113378221181848`) returning **400 logged-out** (while `web_profile_info` 200 and
   one cursor page `doc_id=7950326061742207` 200 came through). Net: logged-out yields the
   **first batch only** — the initial `web_profile_info` page plus ~one cursor page, a few-dozen
   most-recent media, each carrying `video_view_count` — then walls. The exact clean
   @hyram-only depth and date-window were **not isolated**: the wall injects suggested/related
   content, contaminating a raw shortcode/`taken_at` scrape (observed 70 mixed shortcodes
   spanning 2018–2025; newest dated item 2025-06-24). Consequence: logged-out likely covers a
   **short recent window** (~most-recent few-dozen posts) — adequate for low-frequency creators
   and possibly the ~1-month delta, but **fragile** for high-frequency creators or anything
   deeper. **Reliable/deep coverage needs session** — exactly what Phase 2 quantifies.
2. **Sustained cadence / scale — UNTESTED.** One clean `200` ≠ scales. Repeated profile loads
   across ≤5 accounts over time may be **IP-rate-limited** (logged-out has no account to spread
   load — but also no account to ban). This is the H5 lane, not this verdict.

Lesser residuals: `video_view_count` is **cumulative-at-capture**, not a time series — momentum
needs the repeated-over-time harvesting already authorized; **image** posts carry no
`video_view_count` (video/reels only); some values are `0`.

## Phase 2 (retained, not retired) — the session comparison

Phase 2 = re-run **this same disposable probe** with the **owner-provided session**
(`storage_state` exported from an already-logged-in browser; the probe never logs in) to
**compare reachable depth + rate behavior** against logged-out. It is **not** a new capability —
it is the controlled comparison that measures what session actually buys (expected: **depth**,
possibly **rate**, almost certainly **not** new fields). Residual (1) is now resolved in the
**walls-early** direction — logged-out gives only the first batch — so Phase 2 is **justified**:
measure how much depth session adds past the logged-out first-page wall (and whether it 200s
where logged-out 400'd). The logged-out deep-pagination test is **done**; the session run is the
remaining delta, and it needs the owner's `storage_state` export.

## Build reframe (deferred — separate authorized lane, not this finding)

If depth proves sufficient: extend the **existing logged-out IG calls runner** to capture the
`web_profile_info` + grid `graphql/query` response bodies during the profile load it already
performs, parse `video_view_count` per `shortcode`, and attach to the call slices. This needs the
browser adapter (or the IG runner) to **expose response bodies** (the current `browser_snapshot`
returns rendered DOM + screenshot only). Logged-out throughout; no session wired into the core
runner. **Not authorized by this finding** — it records feasibility, not a build go.

## Limitations / non-claims

n=1 account, 3 reels, one logged-out run. A feasibility GO on **reachability**, not an
at-scale, multi-account-over-time, or depth-sufficiency validation. Not authorization, not a
build spec, not validation/readiness/acceptance, not legal advice. The carve-out's posture
(≤5 accounts, ~1-month window, repeated-attended, 10-year bounded retention + takedown) governs
any downstream use.

## Evidence

Raw capture (gitignored, disposable): `orca-harness/_test_runs/reel_probe_logged_out/`
(`SUMMARY.json`, `profile.html`, `reel_01..03.html`, `bodies/` incl. the `web_profile_info` and
`graphql/query` 200 payloads with the `video_view_count` values cited above). Probe script:
`orca-harness/_scratch/reel_viewcount_probe.py` (uncommitted throwaway).
```
