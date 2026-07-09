```yaml
retrieval_header_version: 1
artifact_role: build architecture decision/plan (non-authorizing; planning-only)
scope: >
  Target build architecture for operationalizing IG wind-caller (WindCaller) CALLS (Call) self-capture
  (per-item post + reel caption + engagement) on attended, logged-in, own operating/capture
  accounts (≤10 ceiling / start-5); subject-creator roster uncapped (all creators in
  vertical). Decides how to COMPOSE the existing authenticated-browser primitives
  plus the bounded IG-specific delta, names the few genuinely-architectural choices,
  separates implemented capability from owner-confirmation gaps, and gates the first
  build shape on the H5 cadence probe. Downstream of the IG
  capture-feasibility recon.
use_when:
  - Scoping or authorizing the IG calls-capture build.
  - Checking what already exists vs what is net-new for IG capture.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_wind_caller_capture_feasibility_recon_v0.md
  - docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md
  - docs/decisions/wind_caller_calibration_carveout_v0.md
stale_if:
  - The authenticated-browser adapter / auth_state / cadence primitives change shape.
  - The H5 cadence probe result flips the A2 fork (plain-headless vs session+anti-detect).
  - The retention posture changes again (set 2026-06-14 to a 10-year horizon + takedown-on-request via the carve-out).
status: PLANNING_DRAFT — pre-scoping; not a build authorization
```

# IG Wind-Caller Calls-Capture — Build Architecture (v0, planning)

## Headline: compose existing primitives + a bounded IG delta

A 3-lens architecture pass (read-only subagents) + home-model verification against primary
source found the **single-URL authenticated-browser primitives already exist, are tested/reviewed,
and have bounded build authority.** The IG work composes those primitives. The multi-item
person-level loop, IG reel response-read, and retention were **owner-confirmation deltas** — now
**confirmed 2026-06-14** (see Authorization map: bounded ≤5-account rotating set, ~1-month window,
repeated-attended, reel in-context JSON in / video bytes out, 10-year retention + takedown-on-request).
*(Superseded 2026-06-15: cap counts own operating/capture accounts ≤10/start-5; subject-creator
roster uncapped — see carve-out 2026-06-15 amendment. The "≤5-account rotating set" above is the
2026-06-14 historical receipt; not retro-edited.)*
This **narrows** the recon's earlier build-lane finding (which inspected only
the anonymous `cloakbrowser_snapshot.py` and overstated the gap — see the recon doc's dated
correction) without treating the full IG loop as already authorized.

## Probe finding (2026-06-14, post assumption-gate): headless logged-out reaches IG — calls + stats need NO session

A bounded headless-Playwright probe (the existing `browser_snapshot` adapter, **logged-out**, no
storage_state) against a real creator (`@hyram`) — profile + post + reel — resolved the
assumption-gate's load-bearing unknown ("does headless reach IG like the visible Chrome"):

- **All three SUCCESS, HTTP 200, no login redirect, no bot/challenge block** (rendered DOM
  0.68–0.97 MB each; bounded human-paced reads, no rate-limit hit).
- **Calls render in `og:description` logged-out, headless** — post: `"1,693 likes, 26 comments -
  hyram on … : '…#selflessbyhyram'"`; reel: `"1,047 likes, 43 comments - … : '#ad … #YTTPpartner'"`.
  Caption + likes + comments + date + `#ad` — all present, **no session**.
- **Stats render logged-out** — profile `og:description` = `"724K Followers, 2,339 Following, 321 Posts"`.

**Scope impact (build shrinks):**
- The **moat calls + stats are capturable headless, LOGGED-OUT, via `og:description`** — the
  authenticated-session path (`auth_state` / bootstrap / storage_state) is **NOT required** for the
  core signal. The **A2 fork largely dissolves** (plain headless logged-out already works on bounded
  reads). The browser rung IS still required (stdlib `direct_http` got the shell without
  `og:description`; the browser receives the og tags), but **session is not**.
- The session becomes an **optional enhancement only** (deeper grid enumeration / reel view-counts),
  not a core dependency — so the owner's cookies are not needed for the core build.

**Remaining build-time unknowns (smaller; deferrable, not blockers):**
- Grid permalink enumeration depth logged-out (does the grid scroll-load past the first tranche
  headless, or does the logged-out modal wall scroll) — the loop needs a scroll capability anyway (D1).
- Reel view/play count — still only in the media GraphQL JSON; whether it fires logged-out is
  untested (needs the D3 response-hook). `og:description` already carries likes+comments.
- H5 cadence at repeated/scale — single reads were clean (no block); volume untested.

**Correction to the recon's truncation finding:** the recon's "`og:description` truncates ~59–86%"
used a heuristic "longest non-chrome DOM text node" (635/1594 chars) that over-grabbed non-caption
text (comments/transcript). On re-probe, `og:description` carried the **full** caption for the
tested posts. Genuine og truncation applies only to captions beyond IG's og cap (~125–200 chars) —
real but unmeasured here. So **D2 can use `og:description` for short/medium calls** and fall back to
the DOM caption node only for genuinely long ones.

## What already exists (verified, with paths)

| Piece | Path | What it gives |
|---|---|---|
| Authenticated adapter | `forseti-harness/source_capture/adapters/browser_snapshot.py` | Loads a saved session (`storage_state_path`) into a Playwright context; returns rendered DOM + visible text + viewport screenshot + metadata (`storage_state_loaded`); single URL; `headless=True`; no proxy/scroll/sniff. |
| Session store | `forseti-harness/source_capture/auth_state.py` + `local_secret_store.py` | `AuthenticatedSessionMode`, storage-state JSON validation, metadata-sidecar mode binding, path confinement, size cap. Secret lives in gitignored `_auth_state/`. |
| Interactive login | `runners/run_source_capture_browser_session_bootstrap.py` | `headless=False` + human `input()` — the **owner** enters credentials; the agent never does. |
| Capture→packet | `runners/run_source_capture_authenticated_browser_packet.py` | Loads session → captures one URL → Source Capture Packet; generic login-wall limitation detector; non-claims forbid credential/cookie/storage-state capture; records `access_posture` with `session_mode` (not the secret). |
| Cadence governor | `forseti-harness/source_capture/cadence.py` | `build_cadence_plan(mode="bounded_jitter", window/min_gap/max_gap/seed)` → per-item variable waits; deterministic-per-seed for auditability. Already driven item-by-item in the Reddit batch runner. |
| Tests + review + build-authority basis | `tests/unit/test_source_capture_authenticated_browser_snapshot.py`; `docs/review-outputs/source_capture_authenticated_browser_snapshot_adversarial_code_review_v0.md` (+ post-patch recheck); `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md` (1st-tranche #5 honest/authenticated browser; 2nd-tranche #7 owner-named source adapters). |

## The IG delta (what is net-new)

- **D1 — Multi-item capture loop (NEW runner).** Grid scroll-enumerate (`/p/` + `/reel/` permalinks; reuse the scroll mechanics) → per-item visit → packet, with `cadence.py` `bounded_jitter` between items. The existing runner is single-URL; this is a bounded multi-item runner that *composes* it.
- **D2 — IG extraction (parser).** Caption from the rendered DOM node (the meta truncates ~59–86%); engagement (likes/comments/date/`#ad` sponsorship) from `og:description`/DOM. Parser-over-retrieved-HTML is explicitly allowed by the authorization; cross-check the DOM caption against the meta prefix, flag mismatch, never silently truncate.
- **D3 — Reel view/play count via WARM SAME-CONTEXT JSON.** Not in the page DOM; in the media GraphQL JSON. The closest precedent is the Reddit "load page in-context, then read its own JSON" enrichment pattern, but applying that pattern to IG media GraphQL responses is an **owner-confirmation delta**, not an authorization-scope ruling. Needs a response-read hook the current adapter lacks.
- **D4 — IG block signature.** Extend the generic login-wall detector with IG markers (login-modal / `challenge` / 429-interstitial).

## Genuinely-architectural choices (small)

- **A1 — Loop home.** RECOMMEND a **new runner** composing the existing single-URL adapter N times (lowest lock-in; the adapter stays single-purpose) over a new multi-item adapter. Low stakes; reversible.
- **A2 — The one real fork (H5-gated, not scale-proven).** The anti-detect path (`cloakbrowser_snapshot`, no session) and the session path (`browser_snapshot`, no anti-detect) are **separate**; neither does **session + anti-detect together**. If plain authenticated-headless survives the H5 cadence probe → build the smaller path first, while carrying H5's over-time/multi-account residual. If IG flags it → owner chooses between a combined session+cloak capability (**bigger lift, higher lock-in**) or stopping/de-scoping. **Do not pre-decide; H5 gates the first build shape but does not prove at-scale sustainability.**
- **A3 — Reel-JSON method scope.** Treat the Reddit warm-same-context-JSON pattern as precedent only. Owner confirmation is required before an IG media GraphQL response-read becomes build scope.

## Doctrine / boundary call: secret-handling is not the new doctrine question

The "no-secret/anonymous" property was a per-adapter property of `cloakbrowser_snapshot`/`direct_http`, never repo-wide doctrine. The authenticated session store is an **already-authorized, already-reviewed** exception with explicit secret confinement (authorization 2nd-tranche invariant: "credentials, tokens, cookies, and storage-state never enter the packet … live in local ignored config only"; runner non-claims say the same). Secret-handling itself does not need a new doctrine decision. The separate boundary question is whether a routine, attended, multi-item, person-level IG capture loop stays inside the wind-caller carve-out and the source-access tooling authorization; that is why the owner-confirmation deltas below remain prerequisites.

## Authorization map (what's covered vs to confirm)

- **Covered:** the existing single-URL authenticated browser snapshot and local session-store mechanics (1st-tranche #5 + 2nd-tranche #7), plus the wind-caller carve-out's permission for internal, attended, human-mimicking, own operating/capture accounts ≤10 (start-5) calibration capture; subject-creator roster uncapped (all creators in the vertical).
- **Owner-confirmed (2026-06-14):** (i) **multi-item loop = bounded capture unit** — ≤5 accounts at any one time (rotating / no fixed named list), **recent ~1-month window**, **no full-history backfill**; **repeated _attended_ capture over time is authorized** (to build the durable time-series) and stays **attended — not a standing/scheduled crawler**; (ii) **reel view/play count via in-context (warm-same-context) JSON = in scope; video/image bytes out**; (iii) **retention = 10-year bounded horizon + immediate takedown-on-request**, per the carve-out's dated 2026-06-14 horizon-setting (`docs/decisions/wind_caller_calibration_carveout_v0.md`) — stays within the signed time-bounded posture. *(Superseded 2026-06-15: cap counts own operating/capture accounts ≤10/start-5; subject-creator roster uncapped — see carve-out 2026-06-15 amendment. The 2026-06-14 "≤5 accounts at any one time" text above is the historical owner-confirmation receipt and is not retro-edited.)*
- *(direction_change_propagation 2026-06-15: carve-out 2026-06-15 amendment redefines the cap —
  the ≤10/start-5 ceiling counts OUR OWN operating/capture accounts; the subject-creator roster is
  uncapped (all creators in the vertical); active=attended/passive=bounded-self-terminating method
  posture now explicitly defined. YAML scope header, Covered cell, and Cadence governor updated to
  reflect. Dated 2026-06-14 receipts above are forward-noted, not retro-edited.)*

## H5 gate (the build's premise — run before scaling)

Bounded ~20–30-item slice on ONE owner-confirmed account at full `bounded_jitter` cadence, BEFORE any full-account walk. Abort signal = login-wall modal / IG `challenge` / HTTP 429 / `access_blocked`. Pass = sample completes clean, captions non-empty, engagement parsed. This **gates A2 for the first build shape** (plain-headless first vs stop/escalate to session+anti-detect), but it does **not** prove repeated, over-time, multi-account sustainability. Goal: do not build the full walk then discover cadence fails.

## Cadence governor (reuse `cadence.py`)

`bounded_jitter`: inter-item ~8–45 s jitter; inject a long 90–180 s pause every ~5–9 items; randomize visit order; **per-session ≤40 items; ≤2 sessions / ≤60 items per day; ≤10 of OUR OWN capture/operating accounts total (ceiling; ops start ≤5) — this cap counts our own accounts, not the subject-creator roster which is uncapped**; deterministic-per-seed for auditability; **no scheduler entrypoint** (operator launches each attended run). These are planning ceilings, not entitlement to exhaust every account: one account with N posts implies one grid walk + N item visits, so the owner-confirmed H5 result and stop-on-block behavior govern how far any attended run proceeds.

## Record boundary

Per-item → **Source Capture Packets** via the existing `write_local_source_capture_packet` (one packet per item, or one packet with N `SourceCaptureSlice`s). The calibration ledger is a **downstream consumer** of packets. **ECR / Cleaning / Judgment schema design is OUT** (confirmed by the runner non-claims + the recon).

## Next steps (each gated)

1. `workflow-implementation-scoping` over D1–D4 + A1 (read-only route; STEP-*).
2. ✓ Owner confirmed the three deltas + retention (10-year horizon + takedown-on-request), 2026-06-14.
3. **H5 gate probe** (bounded) → gates the first A2 build shape; at-scale sustainability remains a residual until exercised.
4. Bounded build authorization → build the delta → full offline contract suite green before any green claim.

## Frozen implementation route (2026-06-14) — for a fresh `/fused` implementation turn

`/fused` scoped this and paused at the implementation gate for **context-risk** (do not write new
capture code at the tail of a very long thread; this lane "previously shipped capture code on
partial tests"). The route below is frozen; a fresh turn is pure execution. Code lane prepared:
worktree `.claude/worktrees/ig-calls-capture-build`, branch `ig-calls-capture-build` off
`origin/main` (`96eb1ad`); harness venv with Playwright+chromium installed: `forseti-harness/.venv`.
Scope = the verified **logged-out** build above (no session/auth).

- **STEP-01 — parser (pure, offline).** NEW `source_capture/ig_calls_parse.py`:
  `parse_ig_og_description(s)` → `{caption, likes, comments, date, is_ad}`;
  `extract_item_permalinks(rendered_dom)` → `/p/` + `/reel/` permalinks. NEW
  `tests/unit/test_ig_calls_parse.py` from the recon's observed `og:description` fixtures. No deps.
- **STEP-02 — scroll on the headless engine.** Add bounded `scroll_passes`/`scroll_step_px`
  (default 0 → existing single-URL contract unchanged) to `adapters/browser_snapshot.py`'s engine,
  mirroring `cloakbrowser_snapshot.py`'s scroll loop. Existing browser_snapshot tests must still pass.
- **STEP-03 — the runner.** NEW `runners/run_source_capture_ig_calls_packet.py`: load profile
  (browser_snapshot, logged-out, scroll) → `extract_item_permalinks` → per item: load →
  `parse_ig_og_description` (+ DOM-caption fallback when og looks truncated) →
  `cadence.build_cadence_plan(bounded_jitter)` between items →
  `writer.write_local_source_capture_packet` (compose the authenticated runner's packet pattern
  **minus** `auth_state`) → IG block-detection (login-modal/`challenge`/429) → per-session item cap.
  NEW unit tests (monkeypatch `fetch_browser_snapshot_capture` with fixture-DOM fakes; assert
  packets, cadence applied, block-detection, cap; no live deps).
- **STEP-04 — validation.** FULL offline contract suite green (`forseti-harness/.venv` pytest — full
  suite, not feature-only). Then a bounded LIVE `@hyram` check (logged-out, ≤3 items, human-paced)
  → gitignored `_test_runs/`. **No green claim without the full suite green.**
- **STEP-05 — land.** Commit + PR on `ig-calls-capture-build`, then the **recommended adversarial
  review** (`after_all_steps_pre_closeout`, target = the new runner + parser) via
  `workflow-delegated-review-patch`.

DEFERRED (record, do not build): D3 reel view/play count via GraphQL response-sniff; session/
`auth_state` enhancement (only if logged-out grid-scroll depth proves walled); H5 sustained cadence.

## Non-claims

Planning draft. Not a build authorization, not validation/readiness, not a doctrine change, not an authorization-scope ruling (the owner adjudicates the three deltas), not at-scale or multi-account-over-time proof, not ECR/Cleaning/Judgment design. The existing primitive claims are verified against primary source at the paths cited; the authorization mapping is an advisory reading of the cited decision, carve-out, and recon residuals, not an owner ruling.
```
