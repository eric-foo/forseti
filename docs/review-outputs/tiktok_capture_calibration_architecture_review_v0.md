# TikTok Capture Calibration — Architecture / Scoping Memo v0

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: Read-only architecture/scoping plan for a smallest-complete TikTok public creator/video/comment capture calibration lane supporting anti-bot / data-integrity analysis.
review_type: architecture_scoping_memo
review_date: 2026-06-21
reviewer: Claude Opus 4.8 (read-only planning; 3 read-only recon subagents)
worktree: C:/Users/vmon7/Desktop/projects/orca/.claude/worktrees/brave-maxwell-69cf0f
expected_branch: claude/brave-maxwell-69cf0f (off main @ 6f79445e)
hash_verification: not_performed (planning memo, not a pinned-hash code review; source basis = read-only recon)
edit_permission: read-only planning; edits confined to this memo only, no other source files touched, no live TikTok run
commissioned_by: docs/prompts/handoffs/tiktok_capture_calibration_architecture_prompt_v0.md (codex/social-capture-browser-calibration-ig-only @ a0f42467)
hardening_pass: de-correlated adversarial artifact review-and-patch (repo mode), 2026-06-21 — findings AR-01..AR-06 accepted, CA-adjudicated with citations re-verified; record at docs/review-outputs/tiktok_capture_calibration_architecture_review_findings_v0.md
authored_by: Claude Opus 4.8 (Anthropic)
reviewed_by: unrecorded (non-Anthropic delegate; operator did not record model+version)
authority_boundary: retrieval_only
```

---

## Method note

Read-only architecture planning. Source basis: three read-only recon subagents over `AGENTS.md`, the workflow overlay, the capture toolbox (playbook, recon index, anti-block ladder, embedded-payload weapon, fixture-admission criteria), the Instagram (IG) capture precedent (architecture docs + harness code + tests), and a repo-wide TikTok presence sweep. Citations are `path:line`, repo-relative. Claims about TikTok's *external* surfaces that cannot be verified from this repo are labeled `HYPOTHESIS_FOR_PROBE` and are **not** architecture facts; official-API eligibility/scope is likewise a probe-time docs check, not a repo-proven route. This memo is a probe-design plan in the house grammar; it grants no capture/build authority and asserts no validation or readiness.

---

## 1. SOURCE_CONTEXT_READY

**`SOURCE_CONTEXT_READY`.**

All files named in the prompt's `open_next` and Source-Gated Load Contract exist in this worktree and were read: `AGENTS.md`; `.agents/workflow-overlay/{README,source-loading,safety-rules}.md`; `orca/product/spines/capture/core/source_capture_toolbox/{source_capture_playbook_v0,capture_recon_index_v0,README}.md`; the IG architecture docs (`orca_creator_momentum_pipeline_architecture_v0.md`, `orca_creator_monitoring_policy_architecture_v0.md`, `ig_capture_shape_contract_spec_v0.md`, `ig_wind_caller_calls_capture_build_architecture_v0.md`, and the IG probe-recon set); the source-capture harness (`orca-harness/source_capture/**`, runners, and IG tests); and the anti-block / embedded-payload / fixture-admission toolbox docs. The required TikTok presence sweep (`tiktok`, `tik_tok`, `tik-tok`, `TikTok` across `docs/`, `orca/product/`, `orca-harness/`) was run. No required file failed to read.

> Note on commissioning context: this lane is `claude/brave-maxwell-69cf0f` off `main`, **not** the IG-only worktree named in the prompt. The IG-only worktree's "dirty IG comments patch" is not present here and was not needed — all planning sources are committed on `main`. No IG files were touched.

---

## 2. ADJUDICATED_CURRENT_STATE

**Headline: TikTok is product-authorized ("GO") but technically un-reconned. There is no working route and no TikTok-specific code. A calibration lane must *probe to discover* a route; it cannot inherit one.**

**(a) No TikTok-specific harness code exists — verified.** `orca-harness/source_capture/` has adapters/modules for direct-HTTP, anti-blocking-HTTP, archive.org, archive.today, browser-snapshot, cloakbrowser-snapshot, media-asset, publisher-history, reddit-api, and Instagram (`ig_calls_parse.py`, `ig_momentum_harvest.py`, `ig_projection.py`) — **no `tiktok*` / `tik_tok*` file** (`Glob **/*tiktok*` and `**/*tik_tok*` → none; `grep tik[_-]?tok orca-harness/**/*.py` → zero matches). Every TikTok string under `orca-harness/` is a literal `tiktok.com` link inside a raw Wayback-captured `.../raw/02_archive_snapshot_body.bin` body in unrelated beauty-brand cases — **capture data, not code**.

**(b) The capture playbook treats TikTok as the first *intended* probe target, speculative until probed; the recon index is the fresher source for IG's later probe status.** The playbook's older method text says "TikTok is the first *intended* probe target" and still groups TikTok/Instagram as unreconned social cards (`source_capture_playbook_v0.md:47-49`, `:288-290`). The recon index now refines that: Instagram is probed, while **TikTok has no technical recon at all** (`capture_recon_index_v0.md:166-173`). Per-source recipe cards "are authored BY probes... not here" (`source_capture_playbook_v0.md:47-49`, `:266-269`); "Recipe cards are not yet authored" (`:296`).

**(c) The recon index says TikTok has zero technical recon.** "**TikTok has no technical recon at all**... Any TikTok recipe card is **speculative** until probed; social surfaces carry the heaviest ToS/auth-wall/anti-bot posture... No media/video capture recipe exists either" (`capture_recon_index_v0.md:166-173`). TikTok appears in **no row** of the per-archetype index tables — only in the absence/coverage prose. The absence is "a **sweep result**... not a proof that none could exist" (`:184-186`).

**(d) The product-authorization-vs-technical-recon contradiction — stated precisely, and acknowledged in the authorizing doc itself.**
- *Authorization side:* "**TikTok live capture: GO.** Owner words: 'oh tiktok live was ratified to be a GO'" (`docs/decisions/orca_consumer_demand_ratification_decision_memo_v0.md:79-81`), re-confirmed "'2 - go', 2026-06-12" (`:89`); mirrored in `docs/decisions/orca_product_thesis_consumer_demand_v0.md:431-433`.
- *Technical side:* no TikTok recon; speculative until probed (`capture_recon_index_v0.md:167`; `source_capture_playbook_v0.md:289-290`).
- *The reconciliation is in the GO doc:* "no record on this branch shows the prior GO ratification — the capture recon index still calls TikTok/IG recon speculative and the probe-lane status... was live-NO-GO — so the GO is recorded here on the owner's current word, and the owning capture-lane records... owe their own dated alignment" (`orca_consumer_demand_ratification_decision_memo_v0.md:82-87`); evidence row: "PARTIAL at thesis prep (archive GO-fidelity / live NO-GO legal); owner ratified TikTok live = GO 2026-06-12... lane-record alignment pending" (`orca_product_thesis_consumer_demand_v0.md:587`).

**Adjudication:** the owner GO is a *product-authorization / risk-acceptance posture* — it removed a ToS/policy stop. It is **not** proof of capturability and **not** a working technical route. The capture-lane records still report NO-GO/speculative and explicitly "owe their own dated alignment," which as of this read is **not yet done**. Treat the GO as authorization posture only; the technical route is unproven and must be probed.

**(e) Even the closest precedent (IG) does not cover TikTok's hardest problem.** TikTok is video-first; there is "no media/video capture recipe" anywhere (`capture_recon_index_v0.md:173`), and IG recon covered caption text + stats, not media bytes. Anti-bot capability is "authorized but not yet proven" — fidelity "expected, not demonstrated" (`source_capture_playbook_v0.md:203-204`, `:291-293`) — and TikTok carries "the heaviest... anti-bot posture" (`capture_recon_index_v0.md:172`), so that gap is most acute here.

---

## 3. TARGET_CAPTURE_SHAPE

Fields to pursue, grouped per the prompt, each marked **source-visible** (defensible to attempt) or **`HYPOTHESIS_FOR_PROBE`** (unverifiable from repo; confirm live). All pursued under the IG capture-shape contract's typed-posture rule: **each metric records a typed value + a typed availability posture + coverage boundary, so absence is never stored as an observed value (never an observed `0`)**; value present iff posture = `observed`. Identity must be source-native and stable, never just the mutable username; for TikTok this is a **target invariant, not a proven field**. If a probe cannot expose a stable user/video/comment id, the packet is identity-incomplete rather than silently keyed by handle (`ig_capture_shape_contract_spec_v0.md:36-58`, `:81-89`; `source_capture/models.py:128-137`).

**PROFILE** — handle/`@username` (**source-visible**, in URL); stable native user id, display name, verification flag, follower/following/like/video counts, bio/link (**`HYPOTHESIS_FOR_PROBE`** — IG analogue lives in profile `og:description` meta + an internal `web_profile_info` JSON; TikTok analogue, e.g. an embedded universal-data blob + an internal user-detail endpoint, is unconfirmed); **private flag** (**source-visible as a *gate signal*** — a private account is an access-control wall → out of scope per Step 0; the flag is a breaker trigger, not a harvest target); retrieval/source timestamp (**source-visible**, recorded by the capturer).

**VIDEO** — canonical URL `/@handle/video/<id>` and video id (**source-visible**, in URL); caption (**`HYPOTHESIS_FOR_PROBE`**; expect a meta-truncation-vs-DOM fidelity gap); post timestamp (**`HYPOTHESIS_FOR_PROBE` — critical for the comment-window claim**); play/view count (**`HYPOTHESIS_FOR_PROBE`** — IG's `video_view_count` lived in feed/grid JSON, **not** the permalink page, so TikTok's view-count surface is unknown); likes, comment count, shares, saves/favorites, sound/music metadata, pinned/sponsored/ad indicators (all **`HYPOTHESIS_FOR_PROBE`**); raw evidence anchors — selector / JSON-path + field+value (**source-visible by construction**; required for GO, `source_capture_playbook_v0.md:248-252`).

**COMMENTS** — stable native comment id, commenter handle/display name/id, comment text, like count, reply count, pinned/creator-like/creator-reply markers, top source-returned comments (all **`HYPOTHESIS_FOR_PROBE`**; capture the source's own returned order, do **not** re-rank); comment timestamp/relative-time string (**`HYPOTHESIS_FOR_PROBE`, defensibility-critical**).
- **30-min & 60-min post-relative windows — CONDITIONAL, highest data-integrity risk in the lane.** Defensible **only if** the comment carries a source-native timestamp **and** the video carries a source-native post timestamp at sufficient granularity, with a timezone/epoch basis or another source-native clock basis that makes the arithmetic reproducible. The window is source-derived arithmetic, not capturer-imputed. If TikTok exposes only a coarse relative string ("2d ago", "1w ago"), a date-only value, a locale-dependent string with no clock basis, or any value coarser than the window, a 30/60-min bucket is **NOT defensible** — it fabricates precision the source never asserted, violating the "absence/derived is never an observed value" invariant. **Required posture:** capture the raw timestamp string verbatim, its parse basis/granularity/timezone posture, and the derived field separately; compute the window only as a clearly-labeled *derived* field, and emit `not_applicable` / `unavailable_with_reason` when source granularity or clock basis is too coarse.

**RECEIPTS** (mandatory, `source_capture_playbook_v0.md:260-262`) — raw response/body, source URL, retrieval timestamp, status code, selector/JSON-path anchors, packet limitations, non-claims, plus access classification · routes tried · routes skipped-with-reason · request rate/volume · why-stopped · verdict · routes-now-forbidden. All **source-visible / authored by construction**.

---

## 4. ROUTE_OPTIONS (ranked, cheapest-fit-first per the catalog)

Ranking follows the route catalog's cost order, not capability (`source_capture_playbook_v0.md:179-192`; anti-block ladder is cost-ordered, not capability-ordered, `source_capture_anti_block_ladder_usage_guide_v0.md:46-58`). **Public/logged-out routes are in scope under the bounded Risk posture (human-rate, targeted); own-account, official-API, and vendor rows are catalog/out-of-band checks, not the baseline. The auth/access-control gate is the hard line, never defeated** (`source_capture_playbook_v0.md:64-68`). Every route is a `HYPOTHESIS_FOR_PROBE` for TikTok — none is repo-verified.

| # | Route | Class | Verdict (hypothesis) | Expected evidence | Failure markers | Safety boundary |
|---|---|---|---|---|---|---|
| 1 | Rendered public page HTML (headless browser) | public/logged-out | **PARTIAL candidate** — IG logged-out browser walled deeper content behind a signup modal | JS-rendered profile/video DOM; visible text for block diagnosis | login/signup modal, "verify you are human", empty shell, layout drift | public only; browser rung captures **DOM not raw bytes** |
| 2 | **Embedded hydration state** (a universal/rehydration JSON blob in page source) | public/logged-out | **STRONGEST probe candidate** (house style prizes embedded field+value anchors) | exact embedded field+value anchors; browser-free via rung-1.5 if not render-time-only | blob absent / empty shell / **loud parse miss** | "public via the page, not an auth-gated private API" (`:191`) |
| 3 | oEmbed / public embed endpoint | public/logged-out | **PARTIAL** — likely lacks comments + full counts | sanctioned embed payload (author, thumbnail, limited metadata) | sparse fields; no comments/counts | public, lowest ToS friction |
| 4 | Browser-context XHR / internal public web API (the page's own calls) | public/logged-out *if reachable cookieless-in-browser* | **HIGH-VALUE but CONTINGENT** — if signed+auth-only → **NO-GO** | structured profile/video/comment-list JSON with cursors | 401/403/429, signed-param rejection, empty arrays | **only same-origin, page-emitted requests that work logged-out without invented auth headers/tokens** are in scope; reversing or replaying a private/signed API behind auth = hard stop |
| 5 | Progressive scroll for comments | public/logged-out | **probe candidate for comment depth** (scroll mechanism is capture-proven in-repo) | lazy-loaded comment nodes (IntersectionObserver) | scroll-overshoot that never fires the observer; UI-scroll artifact reading an early wall | public; human-rate; **follow the source's own cursor, not `mouse.wheel`** |
| 6 | Authenticated own-account-only | own-account-entitled | **LAST RESORT / DISCOURAGED** for a *public* analysis lane | same public content via own entitled session | — | **own access only; a human logs in, the agent never enters credentials; G-2 contamination stop — no cookies/storage-state in any admitted packet** |
| 7 | Official TikTok APIs (Display API / Research Tools) | official/API-entitled | **CATALOG / OUT-OF-BAND** — re-check at probe time; Display appears user-authorized/self-content-oriented, Research Tools appear application/eligibility-gated and non-profit/vetted-researcher oriented | metadata/account/video/comment fields if entitlement exists | approval denied, scope excludes target data, comments unavailable, credentials required | do not use as public-web proof; no client secrets/tokens in packets; commercial Orca use likely ineligible unless owner separately proves entitlement |
| 8 | Vendor / paid data | vendor/paid | **CATALOG / OUT-OF-BAND** — fine for a stats series, useless for comment-level integrity | second-hand aggregated stats | — | second-hand only; **verbatim/first-party content must NOT come from a vendor** |

**Honest catalog verdict:** the repo has **no route proven for TikTok video/comment substrate** and **no media/video capture recipe anywhere**. If a probe finds the signal lives **only in the TikTok mobile app with no public web surface**, that is **`CATALOG_GAP`**, not `NO-GO` (`source_capture_playbook_v0.md:284-287`). House-aligned plan: probe **Route 2 (embedded blob)** and **Route 4 (browser-context XHR)** first for profile/video; **Route 5 (cursor-followed scroll)** for comments; treat **1/3** as PARTIAL fallbacks; **6** discouraged-last-resort; **7/8** out-of-band catalog checks only.

---

## 5. SMALLEST_COMPLETE_PATCH_SEQUENCE (if later authorized)

The reuse split is broadly proven by **three sibling families** (IG, Reddit, Retail-PDP), but not as a fixed "four files" promise: packet envelope, writer, packet assembly, cadence, conservative block-shell / rendered-access guards, proxy provenance, and the typed `MetricObservation` substrate are generic and reusable unchanged. Browser snapshot/context-response adapters are reusable unchanged only when the TikTok route is confirmed public/logged-out; `auth_state` is an existing generic primitive only for a separately authorized own-account leg, not for the public baseline. The projection *pattern* is reusable, but each platform's projection remains a satellite because metric vocabulary, identity model, content unit, raw anchors, and source-family guard are platform-specific (`source_capture/models.py:128-137`, `:154-158`; `ig_projection.py:25-33`, `:150-159`). Expect a small satellite family (roughly four to five code files plus a shape-contract spec and fixture tests), with the exact count contingent on the route the probe actually finds. This sequence is a **file-shape hypothesis**, not authorization to build.

**Reused unchanged (generic core, subject to the route gate above):** `source_capture/models.py` (packet envelope `SourceCapturePacket`/`SourceCaptureSlice`/`PreservedFile`/`ReceiptMetadata` + the platform-agnostic `MetricObservation`/`MetricPosture`/`CoverageWindow` substrate); `writer.py`; `packet_assembly.py` (incl. `validate_capture_posture_honesty`); `cadence.py` (`build_cadence_plan`); `block_shell.py` + `rendered_access.py` (conservative block classifiers that never certify content); `proxy_profiles.py`; and the browser adapters `adapters/browser_snapshot.py` (`fetch_browser_snapshot_capture` + `fetch_browser_context_responses`) / `adapters/cloakbrowser_snapshot.py` (site-specific steps live in its `PreCapturePlugin` seam, never the adapter). `auth_state.py` + `run_source_capture_browser_session_bootstrap.py` + `run_source_capture_authenticated_browser_packet.py` are **not** part of the public baseline; they stay available only if a separate owner-entitled login leg is authorized, with the human entering credentials and no cookies/storage-state admitted into a packet.

**New satellite files (TikTok-specific; mirror the named IG file where the eventual route actually matches):**

| STEP | New TikTok file (hypothesis path) | Mirrors IG file | Test area |
|---|---|---|---|
| STEP-01 | `source_capture/tiktok_*_parse.py` (pure DOM/JSON parsers) | `ig_calls_parse.py` | `tests/unit/test_source_capture_tiktok_*_parse.py` |
| STEP-02 | `source_capture/tiktok_momentum_harvest.py` (endpoint/field harvest over `fetch_browser_context_responses`) | `ig_momentum_harvest.py` | unit (fixture JSON) |
| STEP-03 | `runners/run_source_capture_tiktok_*_packet.py` (composes reused primitives; new block markers, metric mapping, slice naming, NON_CLAIMS) | `run_source_capture_ig_calls_packet.py` | `tests/unit/test_source_capture_tiktok_*_packet.py` |
| STEP-04 | `source_capture/tiktok_projection.py` (reuses substrate; TikTok family guard, content_kind, raw anchors, lane) | `ig_projection.py` | `tests/unit/test_source_capture_tiktok_projection.py` |
| STEP-05 | `runners/run_tiktok_creator_momentum_projection.py` (thin CLI; only if a separate TikTok projection satellite is authorized) | `run_ig_creator_momentum_projection.py` | smoke |
| STEP-06 | `.../social_media/tiktok/tiktok_capture_shape_contract_spec_v0.md` (TikTok metric set, identity/conflict policy, coverage claim) | `ig_capture_shape_contract_spec_v0.md` | doc |

**Explicitly NOT portable (must be authored fresh, never copied from IG):** selectors / og:description grammar / permalink regex; JSON paths, endpoints, GraphQL `doc_id`, `X-IG-App-ID`; the IG numeric-id↔username conflict policy and "shortcode" key; IG block markers (`/accounts/login`, "please wait a few minutes"); the IG metric set and its `is_video → not_applicable` view-count rule; the IG "calls"/wind-caller extraction inside the loop (loop *shape* is portable, the extraction is not). The pipeline + monitoring-policy docs already name these as deferred per-platform satellite seams and flag TikTok as the example that "tests the agnostic seam" (`orca_creator_momentum_pipeline_architecture_v0.md:26,50-56`; `orca_creator_monitoring_policy_architecture_v0.md:153-170`).

**Validation pattern (mirror the IG test discipline, no-live smoke):** inject fake adapter results built from observed TikTok fixtures; capture `sleep_fn` to assert the cadence sequence without sleeping; read the written `manifest.json` from disk and assert `source_surface`, slice IDs, `receipt_metadata.non_claims`, honest `partial_capture: N/M`, the metric-registry version line, and the typed `metric_observations` (observed value vs `not_applicable` vs `unavailable_with_reason`); assert the no-go paths write **no packet** (exit-code 3 AND `not output_dir.exists()` on login-redirect / no-permalinks / capture-failure); assert secret hygiene (proxy endpoint/creds absent from manifest + raw; only `category=` provenance). The full offline suite must be green before any live check. Gating: the typed-capture runtime surface is owner-gated and manifest-bump-gated in the IG contract (`ig_capture_shape_contract_spec_v0.md:63-67`); a TikTok lane inherits that gate posture.

---

## 6. LIVE_PROBE_GATE (later, human-authorized, public-only)

Modeled on the IG sustainability-probe gate (`ig_logged_out_sustainability_probe_plan_v0.md:132-159,276-316,356-369`) and the playbook's per-operation network-approval rule (`source_capture_playbook_v0.md:44,298`).

**Preconditions (all must hold before any live TikTok read):**
1. **Explicit, bounded owner authorization for *this* probe** — per-operation, never standing. The harness push/PR permission prompts do **not** cover a live external fetch; this needs its own owner go.
2. **Step-0 classification recorded** — target confirmed `publicly-viewable`; any private account or auth-walled surface excluded up front.
3. **Logged-out-first, compliant-pace-first** — no sessions/cookies/stored auth in the baseline. Starting pace hypothesis **~2.5–4 s between reads, never sub-2 s** (owner-adopted IG operating pace), **to be re-measured for TikTok, not assumed transferable**.
4. **Locked subject set** chosen and recorded before the run; no discovery/snowball mid-run.
5. **Bounded ceilings stated** — request ceiling per window, time ceiling, total windows.
6. **Output to gitignored scratch only**; durable summary only if separately requested; **no raw cookies, storage-state, profile paths, proxy creds, or exit IPs in any durable record** (G-2 contamination stop).
7. **Receipt discipline armed** — the run emits the full Measurement Ledger; "no receipt means no strict interpretation."

**Stop conditions (any one halts immediately):** login redirect / signup modal / any auth wall; captcha / "verify you are human" / interstitial in visible text; 429 / rate interstitial / network-security block; any sign the content is access-controlled not public; operator concern; any indication the route reaches a private/signed API behind the auth gate (→ stop, classify NO-GO, do not escalate). After any wall: **stop, fully-quiet cooldown ≥ 60 min, one low-density recovery read, do not keep periodically probing.**

**Default first slice:** authorize the smallest probe — one bounded logged-out read of **one public profile + one public video + that video's first comment page** — record status / bytes / anchor presence, classify GO / PARTIAL / NO-GO / CATALOG_GAP, expand only on a clean receipt.

---

## 7. NON_CLAIMS_AND_RESIDUALS

**This plan cannot yet prove:**
1. **That any TikTok creator/video/comment surface is technically capturable at human-rate.** Owner GO is authorization posture only; there is no recon and no route. The lane must run a real Step-0→Step-3 probe; it cannot inherit one.
2. **The existence, name, or key-path of any embedded universal-data blob (Route 2)**, and **whether TikTok's internal endpoints return public data in a logged-out browser context or require a signed+authed token (Route 4)** — if authed-only, that leg is NO-GO, not a route to push.
3. **Whether comments paginate logged-out via cursor scroll (Route 5)** or wall behind login; **whether an oEmbed surface exists and what it returns (Route 3)**.
4. **The 30/60-min comment-window claim** — defensible only with source-native comment *and* post timestamps at sufficient granularity plus a timezone/epoch or equivalent source-native clock basis; otherwise it fabricates precision and must be emitted as `not_applicable` / `unavailable_with_reason`. Highest data-integrity trap in the lane.
5. **Whether TikTok's public signal lives only in the mobile app** — if so, `CATALOG_GAP`, not NO-GO. No media/video capture recipe exists anywhere in-repo to lean on.
6. **That IG's pace/throttle envelope transfers** — the ~2.5–4 s pace and sticky-throttle behavior are IG facts carried as TikTok *starting hypotheses*, explicitly not assumed transferable.

**Standing residuals / dependencies:**
- The capture-lane record alignment the GO docs say is "owed" (recon index + probe lane updating to the ratified posture) is **pending** as of this read. A planner must not treat the thesis-level GO as a capture-lane technical fact.
- Anti-bot route fidelity is authorized-but-unproven even for non-social sources; TikTok carries the heaviest anti-bot posture, so this is the most acute residual.
- Official TikTok APIs remain only catalog checks until re-verified at probe time; Display-style self/authorized-user scopes, Research Tools eligibility, client secrets, or vetted-researcher status do not prove a public creator/video/comment capture route for Orca.
- TikTok identity semantics are unproven: stable native user/video/comment ids, mutable-handle conflict policy, and comment-author identity posture must be observed before any projection or cross-run series can claim identity completeness.
- Legal/ToS exposure remains a standing residual beyond the owner GO posture; GO records risk acceptance for probing, not legal clearance, platform permission, or commercial route entitlement.
- The named lane `capture-probe-tiktok-demand` is referenced in the thesis but no probe-receipt doc surfaced in this sweep — treat as "named lane, no recovered receipt" (UNVERIFIED).

**Scope non-claims:** read-only planning. No source files edited, no patches applied, no live TikTok run, no auth/access-control wall touched. This memo grants no capture or build authority, asserts no validation or readiness, and is not legal advice. If implementation is later authorized, isolate it on a fresh TikTok branch/worktree off `main` before editing.
