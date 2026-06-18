```yaml
retrieval_header_version: 1
artifact_role: capture recon finding (non-authorizing)
scope: >
  IG reel/video VIEW-COUNT capture-feasibility recon for the creator-momentum /
  wind-caller lane. Records whether a reel's play/view count is capturable, on
  which surface, at which auth state (logged-out vs session), and how deep.
  Probe-first, before any build. Complements the calls-capture recon (captions +
  engagement), which left the reel view-count residual open.
use_when:
  - Deciding whether reel view/play counts need a session/auth path or are reachable logged-out.
  - Scoping a reel-view-count build (where the signal lives; per-reel vs profile-feed vs cursor pagination).
  - Settling the "session-vs-logged-out" question for IG momentum-outcome signal.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/source_capture_toolbox/capture_recon_index_v0.md
  - orca/product/spines/capture/source_families/instagram/ig_wind_caller_capture_feasibility_recon_v0.md
  - docs/decisions/wind_caller_calibration_carveout_v0.md
stale_if:
  - IG changes the profile-feed / grid graphql/query payload shape, the grid doc_id, or moves video_view_count behind auth.
  - A sustained-cadence-at-scale (multi-account, repeated-over-time) probe lands (would close the one remaining residual).
status: RECON_GO_LOGGED_OUT_INCL_DEEP_HISTORY__SESSION_UNNECESSARY__SCALE_CADENCE_OPEN
```

# IG Reel View-Count Capture-Feasibility Recon (v0)

## What this is — and is not

A **capture recon finding**: a real, bounded, disposable probe of whether a reel's play/view
count is capturable, where it lives, at which auth state, and how deep. Run **probe-first,
before any build**, to resolve the residual the calls-capture recon left ("reel view/play count
— in GraphQL JSON, not page DOM").

**Non-authorizing**: not validation, readiness, buyer proof, or a build go. Raw capture lives
only in gitignored `orca-harness/_test_runs/`; probe scripts are disposable, uncommitted
`orca-harness/_scratch/` throwaways. This doc was **corrected once mid-investigation** — see
*Measurement note* — after a UI-scroll artifact produced a false "walls early" reading that the
cursor-following probe overturned.

## Verdict (headline)

**GO, logged-out — including deep history. Session is unnecessary for this signal.**

- The play/view count **is** capturable **logged-out**: `video_view_count`, per media node, keyed
  by `shortcode`, in the **profile-feed JSON** (`web_profile_info` + the grid `graphql/query`
  pagination) — **200**, no cookies, no auth.
- **Depth is deep, not shallow.** Following the grid's own `end_cursor` via the graphql query,
  logged-out paginated **25 pages, every one `200`**, reaching **365 media back to 2017-08-22**
  (179 with view counts), **no login wall, no `429`**. The grid's `has_next_page:true` +
  `end_cursor` are returned **logged-out**.
- **Session buys nothing.** The same probe with the owner's session was **byte-identical** —
  same 365 media, same dates, same `200`s. Not depth, not fields, not rate (to this volume).
- The count is **not** on the reel permalink page — it is a **profile-feed / grid-pagination**
  artifact.

Consequence: a build is logged-out, **no session wired in**, and harvests `video_view_count`
from the profile-feed + cursor-paginated grid responses the calls enumeration already walks.

## Probes run (2026-06-14, `@hyram`, headless)

1. **Per-reel feasibility** — 3 reels (`DF3CdyJv79A`, `DEntAFPpiCv`, `DCM8psIJXl0`), exhaustive
   capture (all response bodies + full HTML + `/embed/`, five count-key variants plain+escaped).
   Result: **no count on the reel page**; count present in the **profile-feed** payload fired
   during the profile load, keyed by `shortcode` (all 3 targets present).
2. **UI-scroll depth (v1, v2)** — `mouse.wheel` pagination. **Discarded as confounded** (see
   *Measurement note*): falsely read an early wall.
3. **Cursor-following depth (valid)** — follow the grid `end_cursor` via `graphql/query`
   (`doc_id=7950326061742207`) from inside the page context, logged-out vs session. Result above.

## Where the signal lives

- **Reel permalink page (`/reel/<code>/`): no count, logged-out.** A/B/C surfaces all empty; no
  login redirect, no `429`. (The "logged-out gives nothing" intuition was right *about the reel
  page* — but wrong about the profile feed.)
- **Profile-feed JSON: count present, logged-out, `200`.**
  - `GET /api/v1/users/web_profile_info/?username=hyram` → **200 cookieless** (browser context),
    media nodes with `video_view_count` (e.g. 3995, 26542, 52303, 86640, 105479).
  - `GET /graphql/query` grid pagination (`doc_id=7950326061742207`, `id`=`5802114508`) → **200**,
    returns `video_view_count` per node **plus `has_next_page` + `end_cursor`** for deep paging.

## Correction to the prior IG recon

The calls-capture recon recorded `web_profile_info` as **"API 429 cookieless → 200 logged-in"**.
This probe **refines** it: in a real **browser context** (IG's `X-IG-App-ID` + web headers),
`web_profile_info` returns **200 cookieless** with `video_view_count`. The earlier 429 was the
**header-less `direct_http` rung**, not a browser-context XHR — both can be true. Net: the
momentum-outcome signal is **not** behind an auth wall.

## Measurement note (why the verdict was corrected)

The depth question was first probed by **UI scroll** (`mouse.wheel`) with a DOM login-wall
heuristic. That produced a **false "walls early on pass 1"** reading, from two artifacts:
(a) the `role="dialog"` + "Log In" heuristic fired **regardless of auth** (it also "walled" the
logged-in run); (b) `mouse.wheel` **never triggered IG's infinite-scroll observer** in headless,
so both runs stalled at the ~70-item initial load — *identical logged-out and session results
were the tell*. Switching to the grid's **own `end_cursor` via the API** (the correct mechanism)
showed deep, unwalled logged-out pagination. This is the capture-recon index's **Pattern 1**:
*"blocked/limited" is a hypothesis — escalate the interaction or use the right mechanism before
recording a NO-GO/limit.* The false reading and its committed correction are left visible
on this lane's history on purpose.

## Open residual (one, honest)

- **Sustained cadence at scale — UNTESTED.** The deep pagination above was a **single profile**,
  25 pages at ~1.2 s spacing, **no `429`**. That is clean for one deep walk, but it is **not**
  the H5 question: repeated harvesting across many subject creators using ≤10 of our own
  capture accounts (start ≤5) **over time** may be IP-rate-limited.
  Logged-out has no account to ban (good) but no account to spread load (risk). This stays the
  **H5 lane**, not this verdict.

Lesser residuals: `video_view_count` is **cumulative-at-capture**, not a time series — momentum
needs the repeated-over-time harvesting already authorized; **image** posts carry no
`video_view_count`; some values are `0`. The probe's own auth-confirmation check was unreliable
(reported logged-in in both conditions), so the session run's *activation* was not independently
verified — **moot**, since the **logged-out** result alone is sufficient and the session
condition added nothing observable.

## Session lane — retired for this purpose

The deferred "session/auth enhancement" lane was gated on *"only if logged-out grid-scroll depth
proves walled."* It did **not**: logged-out reaches deep history via cursor pagination, and the
session run was identical. **Retire the session lane for reel view-counts.** (Re-open only if the
H5-scale probe shows logged-out is rate-walled where a session sustains more — a different
question from depth.)

## Build reframe (deferred — separate authorized lane, not this finding)

Logged-out throughout, no session. Harvest `video_view_count` from the `web_profile_info` +
cursor-paginated grid `graphql/query` responses (follow `end_cursor`) during the profile
enumeration, attach per `shortcode` to the call slices. Needs the runner to **capture response
bodies** and **follow the grid cursor** (the current `browser_snapshot` returns rendered DOM +
screenshot only). **Not authorized by this finding** — it records feasibility, not a build go.

## Limitations / non-claims

n=1 account (`@hyram`), one sitting. A feasibility GO on **reachability + single-profile depth**,
not a multi-account-over-time or sustained-cadence validation. Not authorization, not a build
spec, not validation/readiness/acceptance, not legal advice. The carve-out posture (≤10 own
operating/capture accounts (start ≤5), subject-creator roster uncapped within the vertical,
active = attended / passive = bounded self-terminating, ~1-month window, repeated-attended,
10-year bounded retention + takedown; carve-out 2026-06-15 amendment) governs downstream use.

*(direction_change_propagation 2026-06-15: carve-out 2026-06-15 amendment redefines the cap — the
≤10/start-5 ceiling counts OUR OWN operating/capture accounts, NOT subject creators; the
subject-creator roster is uncapped (all creators in the vertical); active = attended /
passive = bounded self-terminating method posture defined. The H5 residual and the non-claims
carve-out-posture reference above were updated to match. The n=1 `@hyram` probe facts and the
logged-out reachability findings are factual records and remain untouched.)*

## Evidence

Raw capture (gitignored, disposable) under `orca-harness/_test_runs/`:
`reel_probe_logged_out/` (per-reel + profile-feed `video_view_count` payloads),
`reel_cursor_logged_out/` and `reel_cursor_session/` (`CURSOR_SUMMARY.json` — 365 media / 25
pages / back to 2017-08-22, identical across auth states). Probe scripts (uncommitted throwaways)
under `orca-harness/_scratch/`: `reel_viewcount_probe.py`, `reel_cursor_depth_probe.py`
(`reel_depth_probe*.py` = the discarded UI-scroll attempts).
```
