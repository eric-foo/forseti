```yaml
retrieval_header_version: 1
artifact_role: capture recon finding (non-authorizing)
scope: >
  First IG (Instagram) capture-feasibility recon for the creator-momentum /
  wind-caller (WindCaller) lane. Records, for the owner's OWN account first, whether and at
  which rung the wind-caller signal (public "calls" (Call) = post captions + public
  stats) is capturable via an attended, logged-in, human-mimicking automated
  session, and whether Social Blade (free) covers the stats series. Locks the IG
  capture architecture's open rung / substrate / self-capture-vs-buy choices.
use_when:
  - Choosing the IG capture rung, substrate, or self-capture-vs-buy split.
  - Checking whether IG already has a worked recon before re-probing.
  - Onboarding the IG wind-caller calibration capture path.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
  - docs/decisions/wind_caller_calibration_carveout_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
stale_if:
  - IG changes its profile/post substrate (og:description meta, web_profile_info API shape).
  - The owner moves to commercial scale (triggers licensed/bought-data posture for stats — non-negotiable per the carve-out).
  - A harness-native authenticated-browser capability is built (would re-open the "calls self-capture is human-driven only" residual).
  - Tier-2 (audience-graph / cross-platform stitching) is later activated under its own gate.
status: RECON_COMPLETE_DEMONSTRATED_GO
```

# IG Wind-Caller Capture-Feasibility Recon (v0)

## What this is — and is not

This is a **capture recon finding**: a real, bounded, attended probe of whether the IG
wind-caller signal is capturable, at which rung, where it lives, and what to buy vs.
self-capture. It closes the recon index's IG gap (previously "Instagram has no
technical recon at all").

It is **non-authorizing**. It is not validation, readiness, buyer proof, commercial
authorization, Tier-2 activation, or a doctrine change. It records a finding; where a
finding implies a posture change, it is surfaced, not made. Verbatim personal caption
text was viewed live for the demonstration but is **not retained** here
(retention-minimal, internal-only, per the carve-out).

## Verdict (headline)

**GO (demonstrated) — at the attended logged-in browser rung**, with a clean
self-capture-vs-buy split. Demonstrated on the owner's **own** account *and* on **one public
third-party wind-caller** (`@hyram`, US skincare creator — a feasibility probe, not a chosen
calibration subject). Scope honesty: a feasibility GO on n=2 accounts, **not** an at-full-scale
or multi-account-over-time validation (see Diagnosis & gap-closing + Limitations).

- **Calls (verbatim post captions + dated engagement) = SELF-CAPTURE** first-party, via the
  attended logged-in browser. This is the moat signal. **Demonstrated live.** The verbatim
  caption lives in the **rendered post-page DOM caption node** — **not** the `og:description` /
  `og:title` meta, which is a **truncated summary** (observed on a real `@hyram` post: meta 261
  chars vs full DOM caption 635 chars — ~59% dropped). Enumerate posts via **scroll pagination**
  of the profile grid (observed 12 → 48 across 3 human-paced passes).
- **Public stats (follower / following / post counts; and the historical series) = BUY** the
  series from Social Blade (real creator confirmed tracked; free tier carries a **recent daily
  window** — deep multi-month/year history is premium; second-hand is acceptable per the
  carve-out). Current-snapshot stats also come **free alongside the calls** (profile
  `og:description` meta + header), so only the *deeper historical series* genuinely needs Social
  Blade or continuous self-logging.

`direct_http` (the cheapest rung) is **NO-GO for the signal**; a session-bearing browser is
the working rung. Full per-rung verdicts below.

## Posture / authorization (confirmed on entry)

- Controlling carve-out: `docs/decisions/wind_caller_calibration_carveout_v0.md`, **as amended
  by PR #73** — confirmed **MERGED** (merge commit `5ea1241`, merged 2026-06-13; the recon
  worktree is pinned to that commit). The amendment permits **attended automated** capture at a
  **human-mimicking (variable / ADHD-like) cadence** — not uniform machine-rate, not
  high-throughput, not continuous/24-7; no standing or scheduled crawler.
- This probe is the **owner's OWN account** (`@foo_yu_quan`) — the owner's own data, attended,
  logged into IG by the owner (the agent did not and may not enter credentials).
- Bounded (own operating/capture accounts): ceiling ≤10, ops start ≤5, pre-commercial, internal
  calibration only, US-first. Subject-creator roster is **uncapped** — all creators in the
  vertical are in scope for the roster; the account cap counts **our own capture accounts, not
  subject creators.** Tier-2 (audience graph / cross-platform stitching) NOT activated.
  Tier-3 exclusions untouched.
- Method posture: **ACTIVE** (discovery + capture decisions) = attended (human-initiated);
  **PASSIVE** (monitoring already-flagged creators) = human-initiated, time-bounded,
  self-terminating — no discovery during passive monitoring; NOT a perpetual or scheduled
  standing crawler. Faster-than-human cadence; ToS-accepted.
- *(direction_change_propagation 2026-06-15: cap-redefinition — carve-out 2026-06-15 amendment
  records that the ≤10/start-5 ceiling counts OUR OWN operating/capture accounts; subject-creator
  roster is uncapped; active/passive method posture is now explicitly defined. Supersedes the
  prior "≤5 accounts" framing. The 2026-06-14 PR #73 receipt and probe n=2 facts below are
  factual records and remain untouched.)*
- Risk-posture line (`source_capture_playbook_v0.md`): public content is in scope even against
  ToS; **the auth gate is the hard line — own entitled access only.** The own-account logged-in
  read is exactly own-entitled access; no auth gate was defeated.

## Source-gated method (preflight + SOURCE_CONTEXT_READY)

`orca_start_preflight`: AGENTS.md + overlay `README.md` + `source-loading.md` read in task
context. Worktree off fresh `origin/main` (`5ea1241`), pinned at start. Edit permission:
docs-write (finding + index row). Runtime: bounded live IG capture on the owner's own account.
No new committed adapter code.

Sources reference-loaded: `source_capture_playbook_v0.md` (the 6 cross-cutting patterns +
Step-0/1/2/3 method + Risk posture), `capture_recon_index_v0.md`.
Sources source-loaded: the carve-out (merge state confirmed via `gh`),
`source_capture/adapters/direct_http.py`, `source_capture/screening_reddit_read.py` (the
screen-light entitlement-gate pattern), `source_capture/adapters/cloakbrowser_snapshot.py`.

**`SOURCE_CONTEXT_READY`** — with two resolved naming gaps: the commission named the playbook
`capture_investigation_playbook_v0.md` (actual: `source_capture_playbook_v0.md`) and placed
`screening_reddit_read.py` under `adapters/` (actual: one level up at
`source_capture/screening_reddit_read.py`). Both located and read; no content gap.

## Step 0 — Entitlement / access-control gate

| Route | Classification | Disposition |
|---|---|---|
| IG logged-out web (HTML + profile) | publicly-viewable-but-ToS-restricted | in scope (Risk posture; human-rate) |
| IG internal `web_profile_info` API, cookieless | publicly-viewable surface, bot/rate-gated | in scope; gated by session, not auth |
| IG logged-IN **own** account | authenticated — **own entitled access** | in scope (own data; owner logged in) |
| Social Blade free tier | publicly-viewable | in scope (free, second-hand) |

No auth gate was defeated. The owner logged into their own IG; the agent drove the
already-authenticated session.

## Step 1 — Substrate (where the signal lives)

- **Public stats (counts):** carried in the profile page `og:description` meta tag
  (`"<N> Followers, <M> Following, <K> Posts — …(@handle)"`) **and** in IG's internal
  `web_profile_info` JSON API (`edge_followed_by.count`, `edge_follow.count`,
  `edge_owner_to_timeline_media.count`). The API **no longer carries the post nodes** — counts
  only (observed: `recentPosts: []` even on a 200 logged-in response).
- **Calls (verbatim captions + dated engagement):** the **full verbatim caption** lives in the
  **rendered post-page DOM caption node** (a text element; on the probed `@hyram` post the
  longest non-chrome text node = 635 chars). The post-page `og:description` / `og:title` meta
  (`"<likes> likes, <comments> comments - <handle> on <date>: \"<caption>\""`) carries the same
  fields **but truncates the caption** (~261 chars on that post — ~59% loss) and can be **stale**
  (a profile-page meta showed a following-count that disagreed with the live header). So the meta
  is fine for short captions / engagement+date, but **verbatim long-form calls require the DOM
  node**, not the meta. `ld+json` and an `<h1>` caption were **absent** on the probed post — the
  caption is a plain DOM text node, so a **robust caption selector is a real engineering task**
  (the heuristic "longest non-chrome text node" worked here but is not production-robust).
  Post permalinks (`/<handle>/p/<shortcode>/` and `/reel/<shortcode>/`) are enumerable from the
  profile grid, which **lazy-loads on scroll** (12 → 48 over 3 passes on a 321-post account).
- **The grid is an INDEX, not the signal (owner correction, 2026-06-14).** The profile grid yields
  only thumbnails + permalinks. The capturable signal — verbatim caption **and per-item
  engagement** — lives on **each individual `/p/` and `/reel/` page, visited one-by-one.** Reels
  (`/reel/`) are a first-class capture target alongside posts, **not** the same surface as the grid.
  Per-item engagement confirmed in the page: **likes, comments, date, and the sponsorship `#ad`
  flag** (a `/reel/` probe returned `"1,047 likes, 43 comments - hyram on … : \"#ad …\""` — the
  `#ad` flag is exactly the carve-out's sponsorship-disclosure signal). Caption truncation in the
  meta is even worse for reels: **1,594-char DOM caption vs 220-char `og:description` (~86% loss).**
  **Reel view/play count is a residual** — it was **not** in the standalone reel-page DOM text or
  `og:description`; it lives in the media **GraphQL JSON** (`video_view_count` / `play_count`)
  and/or a grid-tile overlay, a targeted extraction **not demonstrated here**.
- **Capture-volume consequence:** because capture is per-item, a full account read is **one grid
  walk + N individual item-page visits** (N up to the post count, e.g. 321 for `@hyram`). That
  multiplies request volume, which makes the human-mimicking cadence discipline (H5) **more**
  load-bearing, not less — it is the dominant open risk for at-scale capture.
- **NOT in the initial logged-out stdlib HTML:** a bare `direct_http` GET returns a ~595 KB JS
  shell with **no** `og:description`, **no** embedded stats/calls — IG serves the meta-tag'd /
  hydrated content only to a browser-like session.

## Step 2 — The probe ladder (receipts; cheapest-first)

Cadence across all live steps: **attended, variable, human-speed** — a handful of bounded
navigations with multi-second settles, one profile, one API call, one post page. No crawler,
no scheduler, no bulk enumeration. Consistent with the amended carve-out.

| Rung | Target | Status / bytes | Signal present? | Verdict |
|---|---|---|---|---|
| **direct_http** (stdlib, cookieless, browser UA) | `instagram.com/instagram/` HTML | **200**, ~595 KB | No stats meta, no embedded calls (only `props`/`csrftoken`/`challenge` markers) | **NO-GO for signal** (reaches shell, not signal) |
| **direct_http** (cookieless) | `web_profile_info` API (±`x-ig-app-id`) | **429** Too Many Requests (both variants) | n/a — bot/rate-gated cookieless | **NO-GO cookieless** (needs a session) |
| **real browser, logged-OUT** (guest session) | `instagram.com/instagram/` | rendered | **Stats render** (header + `og:description`); post grid renders but **caption depth login-walled** by the signup modal | **PARTIAL** (stats GO; calls walled) |
| **real browser, logged-IN own account** | `instagram.com/foo_yu_quan/` profile | rendered, **no login modal** | Stats in header + `og:description`; post permalinks enumerable | **GO** |
| **real browser, logged-IN own account** | `web_profile_info` API (same-origin fetch, session cookies + app-id) | **200** JSON | Structured stats (followers 186, following 267, posts 3, `is_private:false`); **no post nodes** | **GO (stats only)** |
| **real browser, logged-IN own account** | own post page `/p/<shortcode>/` | rendered, no login modal | Caption present in `og:description`/`og:title` (short ≈ 95-char caption — fit fully, so meta == full *here*; likes/comments/date present) | **GO (calls, short)** |
| **real browser, logged-IN, third-party public** `@hyram` | profile `/hyram/` | rendered, **no login modal**, `is_private:false` | Stats render (321 posts / 723K followers); grid lazy-loads on scroll **12 → 48** over 3 passes | **GO (third-party reachability + pagination)** |
| **real browser, logged-IN, third-party public** `@hyram` | post page `/p/<shortcode>/` | rendered, no login modal | **Full caption = 635 chars in rendered DOM** vs **261 chars in `og:description`** (meta truncates ~59%); `ld+json`/`h1` absent | **GO (verbatim calls) — via DOM, not meta** |
| **real browser, logged-IN, third-party public** `@hyram` | **reel** page `/reel/<shortcode>/` | rendered, no login modal | Caption **1,594-char DOM vs 220 meta** (~86% trunc); **likes 1,047 + comments 43 + date + `#ad` flag** in `og:description`; **view/play count NOT in page DOM** | **GO (caption + likes + comments + sponsorship); reel-views = residual (GraphQL JSON)** |

The 429-cookieless → 200-logged-in contrast on the **same endpoint** is the clean proof that the
block was a session/bot gate (Pattern 1: "blocked is a hypothesis"), not an auth wall and not a
true NO-GO. The meta-vs-DOM caption-length gap (Pattern 3: verbatim-vs-paraphrase is a separate
axis) is the proof that the meta tag is a **lossy** substrate for long calls.

## Step 3 — Social Blade (free-tier) commodity coverage

`socialblade.com/instagram/user/instagram` via `direct_http` (logged-out): **HTTP 200, ~80 KB**,
**no Cloudflare/challenge wall**. Markers present: `Followers`, `engagement` (×20), `rank`,
`Daily`, `Future Projections`, charting. → The free tier **carries the stats series surface**
(follower / engagement / rank / daily, with projections).

**Real-creator depth check (`@hyram`, post-review):** `socialblade.com/instagram/user/hyram` via
`direct_http`: **HTTP 200, ~80 KB, tracked = true** (a real beauty wind-caller is covered, not
just the platform account). The free HTML embeds a **recent daily series** (~14 ISO-date rows
observed) plus `Daily`/`Weekly`/`Monthly` framing and charts. So the free tier gives a **recent
rolling window**; **deeper multi-month/year history is premium** (or must be self-logged over
time). Current numeric extraction from the free page was partial (the live current count is
JS-rendered; it is trivially available first-party from IG itself anyway).

Known limitations: deep historical depth + export are **premium-gated**; data is **second-hand**
(aggregated) — so **verbatim call text must still come first-party**, never from Social Blade
(carve-out requirement).
**Verdict: GO (stats commodity, free tier) for a recent window; deep history = premium / self-log.**

## Step 4 — The decision (locks the architecture's open choices)

- **Rung:** a **session-bearing browser** is the working rung. For the **calls** (moat), that is
  the **attended logged-in own-account browser** (own entitled access). `direct_http` is NO-GO for
  the signal; the logged-out browser is PARTIAL (stats only).
- **Substrate:** **stats** = profile `og:description` meta + `web_profile_info` JSON (counts only);
  **calls** = per-post page `og:description`/`og:title` meta (verbatim caption + dated engagement).
- **Self-capture-vs-buy:** **SELF-CAPTURE the calls** first-party (logged-in own account);
  **BUY the stats time-series** from Social Blade free (current-snapshot stats are free alongside
  the calls; only the historical series needs Social Blade). This is the "self-capture the moat,
  buy the commodity" thesis, instantiated for IG.

## Load-bearing finding for the build lane (STOP — not built here)

**CORRECTION (2026-06-14, post architecture pass — verified against primary source):** the original
paragraph below is **overstated and partly wrong** — it inspected only the anonymous
`cloakbrowser_snapshot.py`. A separate **authenticated-browser capability already exists, is tested,
reviewed, and authorized**: `adapters/browser_snapshot.py` (storage_state-aware), `auth_state.py` +
`local_secret_store.py` (session store + secret confinement), `runners/run_source_capture_browser_session_bootstrap.py`
(interactive **human** login) + `run_source_capture_authenticated_browser_packet.py` (session → URL →
packet), and `cadence.py` (`bounded_jitter`) — under
`docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md`. So IG calls
capture **composes the existing capability** plus a small delta (multi-item loop runner, IG
caption/engagement extraction, reel view-count via the authorized *warm same-context JSON* pattern,
IG block markers) — see `forseti/product/spines/capture/core/source_families/social_media/instagram/ig_wind_caller_calls_capture_build_architecture_v0.md`.
It is **compose-plus-small-delta, not net-new**, and most is already authorized; still out of scope
for *this recon*, gated on the H5 probe + implementation scoping + owner-confirmed authorization deltas.

Original observation (preserved, narrower-but-true): The *anonymous* adapter `cloakbrowser_snapshot.py`
launches `headless=True` with `profile_persistence: none` and `storage_state_loaded: False` — *it*
carries no session, so the anonymous adapter **alone** cannot do logged-in capture. What this missed:
the separate authenticated adapter + runners above.

Until that capability exists: IG calls self-capture is **human-driven (attended browser) only**;
the harness can already do the Social Blade stats fetch at the `direct_http` rung today.

**Two build details surfaced by the third-party probe:** (1) the existing CloakBrowser adapter
**already supports scroll pagination** (`scroll_passes` / `scroll_step_px`), which the grid needs
(12 → 48 on scroll) — so enumeration is not the blocker; the **login session** is. (2) The
verbatim caption is a **plain DOM text node** (no `ld+json`, no `<h1>` on the probed post), so the
build needs a **robust caption-extraction selector** — the recon's "longest non-chrome text node"
heuristic worked once but is not production-grade. (3) Reel **view/play counts** are not in the
rendered page; the build would pull them from the media **GraphQL JSON** (`video_view_count` /
`play_count`) the page already fetches.

**What "harness-native" buys — and does NOT (re: "is it automatic?"):** the build would let the
harness load a **saved logged-in session** (storage_state) and **programmatically walk each
post/reel page** to pull caption + engagement — so a human is not hand-clicking hundreds of items.
It is **not** "automatic" in a set-and-forget sense: the carve-out hard-caps it to **attended,
human-mimicking cadence, no standing/scheduled crawler, own operating/capture accounts ≤10
(ops start ≤5) — subject-creator roster uncapped — pre-commercial.** So it is
**automated extraction during an attended run** — a power tool the owner runs, not a crawler that
runs itself. The capture-volume math above (one grid walk + N item pages) is exactly why the
cadence cap, not the mechanics, is the binding constraint.

## Cross-cutting patterns confirmed (recon index spine)

1. **"Blocked" is a hypothesis** — the cookieless 429 was a session gate, not NO-GO (200 once
   logged in). 2. **Locate substrate first** — stats vs. calls live in *different* substrates;
   `web_profile_info` no longer carries posts. 4. **Entitlement gate first** — logged-out is ToS-
   in-scope; own-account is own-entitled; no auth gate defeated. 5. **PARTIAL/NO-GO are first-class**
   — direct_http NO-GO-for-signal and logged-out-browser PARTIAL are honest, useful diagnoses.

## Diagnosis & gap-closing (post-review, 2026-06-14)

After the first own-account write, the verdict was adversarially diagnosed: the original "GO
(demonstrated)" rested on n=1 own account (3 posts) and documented the **meta-tag** caption
substrate, which is lossy. Five holes were named (H1–H5) and a bounded third-party probe
(`@hyram`) was run to close them:

| Hole | Status | Evidence |
|---|---|---|
| **H1** — proved only the own (easiest) account class, not a third-party creator | **CLOSED** | `@hyram` public account renders logged-in with **no login wall** (`is_private:false`); stats render |
| **H2** — caption fidelity rested on the truncating meta tag | **CLOSED + corrected** | meta `og:description` = 261 chars vs **full DOM caption = 635 chars** (~59% loss); verbatim substrate is the **rendered DOM node**, not meta |
| **H3** — no pagination past the first grid tranche | **CLOSED** | scroll grew the grid **12 → 48** over 3 passes; CloakBrowser `scroll_passes` supports it |
| **H4** — Social Blade depth unverified for a real candidate | **CLOSED (nuanced)** | `@hyram` tracked = true; free HTML carries a **recent ~14-day daily window** + weekly/monthly + charts; **deep history premium** |
| **H5** — cadence vs anti-bot sustainability at scale | **RESIDUAL** | ~6 reads across 2 accounts, **no 429s** on the logged-in browser or Social Blade `direct_http`; but **repeated / over-time / multi-account** reads were **not stress-tested** |

Net: the GO holds and is now better-supported (own + 1 third-party), with the calls substrate
**corrected from meta → rendered DOM**. The honest residual is H5 (sustained cadence) plus
full-history enumeration (only 48 of 321 posts loaded) and a production-grade caption selector.

## Limitations / residuals / non-claims

- **Feasibility scope, n=2 accounts.** Demonstrated on `@foo_yu_quan` (own, 3 posts) and `@hyram`
  (third-party, 321 posts). **Full enumeration not run** — only 48 of `@hyram`'s 321 posts were
  loaded (3 scroll passes); the scroll path is proven, the *complete* walk is not.
- **H5 — sustained cadence vs anti-bot not stress-tested.** No rate-limit was hit, but repeated,
  over-time, multi-account capture (what calibration actually does) was not exercised.
- **Verbatim caption needs the DOM node + a robust selector** (no `ld+json`/`h1`); the meta tag is
  lossy (~59% on a post, ~86% on a reel) and can be stale. **[Correction 2026-06-14: those
  truncation deltas were a measurement artifact — the "DOM 635/1594" figures were a heuristic
  "longest non-chrome text node" that over-grabbed comments/transcript, not the caption. A headless
  re-probe showed `og:description` carried the FULL caption for the tested posts; genuine og
  truncation applies only to captions beyond IG's og cap (~125–200 chars). See
  `ig_wind_caller_calls_capture_build_architecture_v0.md` → Probe finding (2026-06-14).]**
- **The grid is index-only; capture is per-item.** Caption + per-item engagement require visiting
  each `/p/` **and** `/reel/` page one-by-one (one grid walk + N item visits per account).
- **Reel view/play count NOT captured** in this recon — absent from the standalone reel-page DOM
  and `og:description`; lives in the media GraphQL JSON (`video_view_count`/`play_count`) /
  grid-tile overlay (targeted extraction not demonstrated).
- **Harness-native logged-in capture NOT built** (see the build-lane finding) — calls self-capture
  is human-driven (attended browser) only until the auth-browser capability exists.
- **Stats deep-history** from Social Blade free is **premium-limited** (recent window only);
  verbatim call text must stay first-party.
- **`@hyram` is a feasibility probe, not a chosen calibration subject.** No calibration record was
  built; only capture-mechanics metrics (lengths, counts, status) were retained — no caption text.
- Not validation / readiness / buyer-proof / commercial authorization / Tier-2 activation / a
  doctrine change. A green fetch is not the gate — this recorded verdict is.

## Next authorized step (candidate, not authorized here)

The first third-party feasibility probe is now done (`@hyram`, above). Remaining candidates, each
needing its own authorization:

- A bounded build to add a harness **authenticated-browser capability** (own session
  storage-state, attended, human-mimicking; scroll pagination already supported; needs a robust
  caption-DOM selector) so calls self-capture is harness-native, not human-driven.
- A **full-enumeration + sustained-cadence (H5)** check on a real calibration set (the residuals
  this recon left open): complete the scroll walk past the first tranche and confirm a
  human-mimicking, over-time, multi-account cadence does not trip anti-bot.
```
