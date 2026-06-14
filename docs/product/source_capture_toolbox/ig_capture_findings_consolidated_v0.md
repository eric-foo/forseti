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
  - docs/product/source_capture_toolbox/ig_reel_viewcount_capture_feasibility_recon_v0.md
  - docs/product/source_capture_toolbox/ig_wind_caller_capture_feasibility_recon_v0.md
  - docs/product/source_capture_toolbox/ig_wind_caller_calls_capture_build_architecture_v0.md
  - docs/product/source_capture_toolbox/capture_recon_index_v0.md
  - docs/decisions/wind_caller_calibration_carveout_v0.md
stale_if:
  - IG moves any signal behind auth, changes og:description shape, the profile-feed payload, or the grid doc_id.
  - The H5 sustained-cadence-at-scale probe lands (closes the one cross-signal residual).
  - The reel-view-count build ships (moves that signal from feasibility-proven to built).
status: CONSOLIDATED — calls+stats SHIPPED logged-out; reel view-count FEASIBILITY-PROVEN logged-out; one residual (scale)
```

# Instagram Capture Findings — Consolidated (v0)

## Headline

**The entire IG wind-caller signal — public "calls" (captions + engagement), profile stats, and
reel/video view counts — is capturable HEADLESS and LOGGED-OUT. No session, cookies, login, or
auth path is needed anywhere.** Two independent attempts to justify a session path (the original
"attended logged-in" recon framing, and a "session needed for reel depth" hypothesis) were both
**refuted by direct measurement**. The authenticated/session lane is **retired** for this signal.

## Signal-by-signal

| Signal | Where it lives | Auth | Status | Source |
| --- | --- | --- | --- | --- |
| **Calls** — verbatim caption + likes + comments + date + `#ad` flag, per post/reel | post/reel page **`og:description`** meta | **logged-out** | **BUILT + validated** (runner; 832 tests pass; live `@hyram` 6/6) | calls recon + build arch; `run_source_capture_ig_calls_packet.py` (merged) |
| **Profile stats** — followers / following / post counts (snapshot) | profile **`og:description`** + `web_profile_info` JSON | **logged-out** | capturable now; **historical series** = Social Blade (free, recent window) or self-logging over time | calls recon + build arch |
| **Reel / video view counts** — `video_view_count` per media | **profile-feed JSON** (`web_profile_info` + grid `graphql/query`), follow `end_cursor` for depth | **logged-out** | **FEASIBILITY-PROVEN** (deep: 25 pages, 365 media back to 2017, no wall/`429`); **build deferred** | reel-viewcount recon (this lane) |
| **Media / video bytes** | n/a | — | **OUT of scope** — never probed; not captured | — |

## Auth posture (the load-bearing conclusion)

- **Calls + stats**: the runner is `logged-out` by construction — *"needs no session"*; non-claims
  include *"not login or session capture"*, *"not proxy or session injection"*.
- **Reel view counts**: the profile-feed JSON (`web_profile_info`, **200 cookieless** in a browser
  context) and the grid `graphql/query` cursor pagination both return `video_view_count`
  logged-out; a session run was **byte-identical** to logged-out.
- **Therefore**: never wire cookies/session into the IG runner. The "session/auth enhancement"
  deferred lane is **retired** (re-open only if the H5-scale probe shows logged-out is
  rate-walled where a session sustains more — a *scale* question, not a *reachability* one).

## Method map (where each signal lives, how to get it)

- **Calls + snapshot stats** → parse the post/reel/profile **`og:description`** meta from a
  headless logged-out browser snapshot. Enumerate items from the profile grid.
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

## Build status

- **Calls capture: SHIPPED** — logged-out runner, parsers, scroll enumeration, cadence, packet
  writer; full suite passes; live-verified. Merged.
- **Reel view-count capture: NOT built** — feasibility proven only. The build would extend the
  logged-out runner to capture profile-feed response bodies + follow the grid cursor, parsing
  `video_view_count` per `shortcode` onto the call slices. Needs the runner to **expose response
  bodies** and **follow the cursor**. **Separate, deferred, needs an explicit build go.**

## Residuals / not-proven

- **Sustained cadence at scale (H5)** — the one cross-signal residual. Single deep walks are clean
  (no `429`), but repeated harvesting across ≤5 accounts **over time** is untested (IP-rate risk;
  logged-out has no account to ban but none to spread load). **Untested.**
- **Reel view counts are cumulative-at-capture**, not a time series — momentum requires the
  repeated-over-time harvesting the carve-out authorizes.
- **Image posts** carry no `video_view_count`; some values are `0`.
- **Media/video bytes** are out of scope and unprobed.
- Probes are **n=1–2 accounts** feasibility GOs, not at-scale validations.

## Posture / carve-out

Governed by `docs/decisions/wind_caller_calibration_carveout_v0.md`: ≤5 rotating public-figure
accounts, ~1-month recent window, no full-history backfill, repeated-**attended** (not a scheduled
crawler), 10-year bounded retention + immediate takedown-on-request. Stats at commercial scale →
licensed/bought-data posture.

## Non-claims

A findings consolidation, not authorization, build spec, validation, readiness, acceptance, or
legal advice. "Shipped" refers to the calls runner's merged + validated state; "feasibility-proven"
is a recon GO, not a built or at-scale claim. Per-doc sources above remain the primary record.
```
