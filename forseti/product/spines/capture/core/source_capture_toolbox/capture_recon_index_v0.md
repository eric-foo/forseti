```yaml
retrieval_header_version: 1
artifact_role: Capture recon consolidation index (non-authorizing)
scope: >
  Consolidates the scattered per-source capture RECON / INVESTIGATION findings across
  the toolbox, data-capture-spine pressure tests, research receipts, and worktree-resident
  lane findings into one index. Records, per source probed, what was found capturable, at
  which runner rung, where the signal actually lives, and any corrected false-diagnosis.
  This index is the evidence base the capture-investigation doctrine + runbook distil from.
use_when:
  - Drafting the source-agnostic capture-investigation doctrine and per-archetype recipe cards.
  - Checking whether a source archetype already has a worked recon before re-probing it.
  - Locating the highest-signal real probe receipts (captured bytes / live-verified verdicts).
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/operating_model/data_capture_harness_operating_model_architecture_v2.md
stale_if:
  - A new source recon lands (this index is append-only until the doctrine supersedes it as the home).
  - The worktree-resident findings (Sephora/Bazaarvoice reviews; Ulta Apollo embedded-JSON) merge to main.
  - The capture-investigation doctrine is authored and adopts the cross-cutting patterns below as its spine.
```

# Capture Recon Consolidation Index (v0)

## What this is — and is not

This is a **non-authorizing index** of the capture RECON / INVESTIGATION findings already
in the repo — the docs that probed a real source to learn **whether and how it can be
captured**. It exists so the capture-investigation doctrine and its per-archetype recipe
cards are **distilled from real probe evidence, not invented**.

It is **not** a build spec, not validation, not an acceptance claim, and not legal advice.
Verdicts below are **as reported by each source doc**, not re-observed here. It governs
nothing; it feeds the doctrine.

## Cross-cutting patterns — the doctrine seed (highest-value section)

These six patterns recur across independent probes. They are the spine the investigation
doctrine should encode.

1. **"Blocked" is a hypothesis, not a verdict — and it is the dominant false-diagnosis.**
   A 403 / empty body / "anti-bot gated" read was *wrong or imprecise* in multiple
   independent cases: Daimler PDFs (direct-HTTP 403 **and** headless 403, yet **visible
   Chrome + the PDF-viewer download button succeeded**); Sephora reviews (worktree:
   "anti-bot gated" → actually a **scroll-overshoot** that never fired the lazy-load
   observer); Teal/WSO (403 first recorded as "content unavailable," later re-diagnosed as
   an anti-bot gate). **Escalate the interaction (real browser context → user-initiated
   action → progressive scroll → proxy/geo) and re-probe before recording NO-GO.** A false
   "blocked" abandons a capturable source.
2. **Locate the signal substrate first; pick the tool second.** Reddit = raw JSON;
   reviews = a first-party-rendered vendor API (Bazaarvoice); SPA state =
   `__APOLLO_STATE__` / `__NEXT_DATA__` (Ulta, worktree); PDF body = a download button.
   The cheapest working rung is a function of **where the signal lives**, so step 1 of
   diagnosis is finding the substrate, not choosing a runner.
3. **Verbatim-vs-paraphrase is a separate axis from reachable-vs-blocked.** WebFetch
   *reaches* M&I/BIWS but returns **paraphrase**, losing layout/packaging fidelity. A
   recipe must record whether a rung preserves source **bytes**, independent of whether it
   gets through.
4. **The entitlement/legal gate is orthogonal to the technical gate and comes first.**
   LinkedIn policy forbids automated capture **regardless** of technical reachability;
   Reddit's API has a commercial-use gate. A NO-GO can be *legal*, not technical. Never
   bypass an unentitled gate even when it is technically trivial.
5. **NO-GO and PARTIAL are first-class, honest outcomes.** Daimler pre-cutoff archive
   returned **no memento exists** → an honest NO-GO; archive *availability* ≠ body
   *retrieval* → PARTIAL. Concluding "not cleanly capturable within boundary" is a
   *successful* diagnosis, not a failure.
6. **The runner ladder is empirically real and cheapest-first.** archive.org →
   direct-HTTP → **(visible) browser** → cloakbrowser+proxy. "Visible browser + a
   user-initiated action" is a genuine escalation rung that defeats headless-detection
   where both direct-HTTP and headless fail (Daimler).

## Index — by archetype (verdicts as reported by each source)

### Reviews
| Source probed | Path | Rung / where signal lives | Reported verdict | Signal |
| --- | --- | --- | --- | --- |
| Sephora PDP reviews **(worktree, pending-merge)** | `orca-cloak-scroll-wt/forseti-harness/docs/source_capture_review_rendering_findings_v0.md` | Bazaarvoice API, first-party-rendered into DOM, lazy-load on **progressive scroll**; bot wall **passed** legitimately | **GO via incremental scroll** (corrects a prior false "anti-bot-gated" claim) | HIGH ⭐ |
| ClickUp on Trustpilot / G2 | `forseti/product/spines/capture/core/operating_model/core_spine_v0_data_capture_spine_pressure_test_review_surface_v0.md` | Live public review text; rating+text+date coupling, reviewer-status labels | Captured; review-surface satellite guidance formalized | MODERATE |

### Forums / threads
| Source probed | Path | Rung / where signal lives | Reported verdict | Signal |
| --- | --- | --- | --- | --- |
| Reddit r/financialcareers (10 threads, 563 rows) | `forseti/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_slot3_reddit_capture_session_v0.md` | Raw JSON → Mechanical Source Projection; row/parent_id/depth; `more_placeholder` visibility | `categorical_handoff_to_ECR` (limited) | HIGH |
| Reddit ECR-consumption probe (old.reddit r/b2bmarketing) | `docs/workflows/reddit_capture_to_ecr_consumption_probe_finding_v0.md` | `run_source_capture_http_packet`, HTTP 200 ~104 KB, 14 comments; `cutoff_posture` param | GO / residual by-design (missing Decision Frame, not a capture defect) | HIGH |
| Wall Street Oasis (7 pages) | `forseti/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_slot3_wso_capture_session_v0.md` | Browser visible-page + Wayback availability; email-unlock prompts visible, **not used** | `categorical_handoff_to_ECR` (partial; no full comment graph) | HIGH |
| Reddit API-pricing threads (r/reddit, r/Devvit, r/apolloapp) | `forseti/product/spines/capture/core/operating_model/core_spine_v0_data_capture_spine_pressure_test_threaded_forum_reddit_api_pricing_v0.md` | Public pages (live fetch blocked → recorded as source-access failure, not boundary); related-chain + package segmentation | Related-chain/bundle preserved; discharge specificity needs tightening | HIGH |
| Reddit offline packet consolidation (parser spec) | `forseti/product/spines/capture/core/source_capture_toolbox/reddit_packet_consolidation_runner_structural_spec_v0.md` | Packet reader; flat comment list + parent_id; closed comment-posture vocab | Packet-first boundary locked; raw packet > parsed text | HIGH (spec) |
| Slot-3 source-quality closeout (Reddit b1/b2 + WSO) | `forseti/product/spines/capture/core/source_capture_toolbox/source_quality_slot3_post_recapture_closeout_v0.md` | Raw JSON + visible HTML (~200 KB cap) | `mini_god_tier_with_visible_limitations` (bounded GO) | MODERATE |
| Reddit thread **DISCOVERY** (screening seam) - find thread URLs without an external index | this row + `docs/workflows/reddit_candidate_intake_old_reddit_search_surface_handling_v0.md` (parse) + `docs/workflows/reddit_capture_to_ecr_consumption_probe_finding_v0.md` (live receipt) + `docs/workflows/screening_read_service_build_receipt_v0.md` (screening-read build receipt) | Reddit-native search/listing surface (`search-title`/`title` -> `/comments/` anchors), direct-HTTP rung; an external search-engine index is the wrong surface | **GO for bounded screening-read service** - listing/thread live-fetch GO; first-act old.reddit search-surface receipt closed 2026-06-21 via `screening_read`; `.json` rate posture remains a human-rate/backoff note | HIGH |

**Reddit thread discovery (screening seam) — working read shape.** *[discovery-spine cross-lane commission, 2026-06-11]*
- **Substrate (pattern 2):** Reddit's *own* search/listing is the discovery surface; the external search-engine index is the wrong surface — the discovery walk's zero-result on `site:reddit.com` queries is expected, **not** a capture gap. Native surfaces: `old.reddit.com/r/<sub>/search?q=…&restrict_sr=on` (+ `&sort=`/`&t=` window), subreddit listings `/new`, `/top?t=`, and their `.json` variants.
- **Rung (pattern 6, cheapest-first):** **direct-HTTP** is already GO on old.reddit *listing* (prior live run: HTTP 200 → 10 candidate thread URLs) and *thread body* (ECR-consumption probe: HTTP 200 ~104 KB). Parse with the documented `search-title`/`title`→`/comments/` anchors, then run the empty-result surface-shape check before any NO-GO (pattern 1: "blocked" is a hypothesis).
- **Entitlement (pattern 4, gate first):** logged-out public old.reddit page reads sit under the owner-authorized public-content posture; the licensed Reddit **Data API** (commercial-use gate) is a *separate* route not needed for discovery. The existing intake doc's "do not call `.json`" hard stop is that lane's *no-live-mode* discipline, **not** a global entitlement bar — but unauthenticated `.json` is rate-limited / ToS-bounded, so treat it as a direct-HTTP-rung route at human rate with backoff.
- **Residual closed / remaining note:** the search surface live receipt was closed 2026-06-21 by the bounded screening-read service (`old.reddit.com/r/beauty/search?q=skincare+moisturizer&restrict_sr=on&sort=new`: HTTP 200, 112317 bytes, 75 `/comments/` markers, no packet/ECR). The `.json` rate ceiling remains a human-rate/backoff note, not a blocker for old Reddit HTML screening reads.
- **Consumer:** the beauty card-set cards 4-6 access caveat. **Update 2026-06-21:** WebFetch-based walkers still cannot fetch `reddit.com` directly, but the orchestrator can invoke `source_capture.screening_read.screening_read(...)` for bounded public Reddit screening reads. Walkers record the need; they do not call the service directly. For public challenge-walled pages, `source_capture.screening_browser_read.screening_browser_read(...)` returns visible text and classifies `block_shell` on visible text, not full DOM.

### Pricing
| Source probed | Path | Rung / where signal lives | Reported verdict | Signal |
| --- | --- | --- | --- | --- |
| OpenAI price payload **(worktree/lane, rung-1.5)** | `orca-rung15-wt` (branch `capture-rung15-openai-payload`, unmerged) | Embedded price payload + token-list certification | Committed-not-merged; narrowed "internally-consistent as-served" claim | HIGH ⭐ (lane) |
| M&I / BIWS | `forseti/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_slot1_mi_biws_capture_session_v0.md` | WebFetch → **paraphrase, not verbatim**; archive metadata known, bodies failed | `visible_stop` + re-capture posture (fidelity loss) | HIGH |
| Teal (tealhq.com) | `forseti/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_slot2_teal_capture_session_v0.md` | **HTTP 403 full-host block** → WebSearch fallback (non-verbatim) | `visible_blocker` + re-capture posture (anti-block/auth needed) | HIGH |

### Docs / changelog
| Source probed | Path | Rung / where signal lives | Reported verdict | Signal |
| --- | --- | --- | --- | --- |
| Kubernetes v1.32 deprecation guide / release blog | `forseti/product/spines/capture/core/operating_model/core_spine_v0_data_capture_spine_pressure_test_docs_changelog_versioned_page_v0.md` | Live docs + GitHub raw + static snapshot; version-page + last-modified coupling | Passed; docs-changelog satellite guidance | MODERATE |

### Archive / history
| Source probed | Path | Rung / where signal lives | Reported verdict | Signal |
| --- | --- | --- | --- | --- |
| Daimler DSU PDFs (pre-cutoff identity) | `docs/research/daimler_advisory_001_source_body_capture_dsu_001_003_receipt_v0.md` | Direct-HTTP **403**; archive.org CDX = **no pre-cutoff memento** | **NO-GO** on pre-cutoff version identity (honest) | HIGH ⭐ |
| Unity Runtime Fee (announce + recapture) | `forseti/product/spines/capture/core/operating_model/core_spine_v0_data_capture_spine_pressure_test_archive_history_recapture_v0.md` | Live + archive.org availability (bodies not fetched); recapture-delta | Archive availability ≠ body; recapture timing posture | MODERATE |

### Docs / PDF body (anti-bot escalation)
| Source probed | Path | Rung / where signal lives | Reported verdict | Signal |
| --- | --- | --- | --- | --- |
| Daimler DSU-001/002/003 PDFs (body capture) | `docs/research/daimler_advisory_001_browser_source_body_capture_dsu_001_003_receipt_v0.md` | direct-HTTP 403 + headless 403 → **visible Chrome + download button = captured bytes** (2.6/1.3/4.1 MB, `%PDF`, SHA256) | **GO via visible browser + user action** (corrected anti-bot diagnosis) | HIGH ⭐ |
| Daimler S1–S7 source acquisition | `docs/research/judgment-spine/harness/v0_14/fixtures/.../source_acquisition_receipt_v0.md` | Canonical issuer 403 → public-mirror + owner-supplied PDF fallback (SHA256 verified) | MIXED GO/NO-GO (canonical-domain bytes residual) | HIGH |

### SPA embedded-state
| Source probed | Path | Rung / where signal lives | Reported verdict | Signal |
| --- | --- | --- | --- | --- |
| Ulta product / Apollo cache **(worktree/lane, DP-002)** | demand-projection lane (`orca-demand-projection-wt`, unmerged) | `__APOLLO_STATE__` cache node; needle from field+value `"productId":"<id>"` | Provenance fix (a) applied in-lane; keep-gate pending | HIGH ⭐ (lane) |

### Browser-automation runner
| Source probed | Path | Rung / where signal lives | Reported verdict | Signal |
| --- | --- | --- | --- | --- |
| CloakBrowser local setup | `forseti/product/spines/capture/core/source_capture_toolbox/cloakbrowser_local_setup_probe_receipt_v0.md` | Local binary (Chromium 146) + API introspection; smoke test | `READY_FOR_ADAPTER_CONTRACT_SCOPING` | HIGH |
| CloakBrowser packet-runner architecture | `forseti/product/spines/capture/core/source_capture_toolbox/cloakbrowser_packet_runner_architecture_v0.md` | API shape from public docs + introspection; no-secret/anonymous seam | `TARGET_RECOMMENDED` (adapter-contract-first) | HIGH (arch) |
| Screening browser read wrapper | `docs/workflows/screening_read_service_build_receipt_v0.md`; code at `forseti-harness/source_capture/screening_browser_read.py` | CloakBrowser render -> visible text only; `block_shell` classified on visible text to avoid residual Cloudflare DOM-script false positives | Implemented on PR branch; no packet / no manifest / no ECR | HIGH |

### Social networks (policy boundary; technical probe largely absent)
| Source probed | Path | Rung / where signal lives | Reported verdict | Signal |
| --- | --- | --- | --- | --- |
| LinkedIn official policy | `forseti/product/spines/capture/core/source_capture_toolbox/linkedin_reddit_source_capture_armory_concurrent_structure_architecture_v0.md` | Policy docs (2026-06-05): scraping/automation forbidden absent authorization | **Boundary-only** — official/API/manual/entitled routes only; no scraping | MODERATE-HIGH |
| Instagram wind-caller — own `@foo_yu_quan` + third-party `@hyram` *(2026-06-14)* | `forseti/product/spines/capture/core/source_families/social_media/instagram/ig_wind_caller_capture_feasibility_recon_v0.md` | Attended logged-in browser (own + 1 public third-party, no wall). **Grid = index only**; capture is **per-item: each `/p/` AND `/reel/` page, one-by-one**. Per item → **full verbatim caption in the rendered DOM node** (meta `og:description` truncates ~59% on a post, ~86% on a reel) + **likes/comments/date/`#ad` sponsorship flag**. Enumerate via **scroll pagination** (12 → 48 / 3 passes). Stats → profile `og:description`/header + Social Blade free (recent daily window; deep history premium) + `web_profile_info` JSON (counts only). `direct_http` NO-GO for signal (200 shell; API **429 cookieless** → **200 logged-in**). | **GO (demonstrated, n=2)** — self-capture calls via DOM (moat), **buy** stats series (Social Blade free). Residual: sustained cadence (H5), full enumeration, robust caption selector, **reel view/play count (in GraphQL JSON, not page DOM)**. Harness-native authenticated capture **already exists** (browser_snapshot + auth_state + runners + cadence, authorized/reviewed); IG = compose + small delta (loop runner, extraction, reel warm-JSON, block markers) — see ig_wind_caller_calls_capture_build_architecture_v0.md. | HIGH ⭐ |
| Instagram reel **view/play count** — `@hyram` 3 reels *(2026-06-14)* | `forseti/product/spines/capture/core/source_families/social_media/instagram/ig_reel_viewcount_capture_feasibility_recon_v0.md` | **Profile-feed JSON** (`web_profile_info` + grid `graphql/query` pagination), **logged-out 200**, `video_view_count` per media keyed by `shortcode` — **not** on the reel permalink page (surfaces A/B/C empty there). | **GO logged-out — incl. deep history.** `video_view_count` reachable **cookieless in a browser context** (refines prior "API 429 cookieless"); cursor-following the grid `end_cursor` paginated **25 pages, all `200`, 365 media back to 2017**, **no wall / no `429`**; **session run byte-identical → unnecessary**. Residual: sustained cadence at scale (H5 / multi-account-over-time). | HIGH ⭐ |
| Instagram creator **discovery** — suggested/related-accounts edge — `@jeremyfragrance` / `@nikkietutorials` / `@hyram` *(2026-06-15)* | `forseti/product/spines/capture/core/source_families/social_media/instagram/ig_creator_discovery_suggested_accounts_recon_v0.md` | **`web_profile_info` JSON** `data.user.edge_related_profiles` — the tolerant **200-cookieless** surface (same as calls/stats/reel-views); node = `username`+`id`+`full_name`+`is_verified`+`is_private`+`profile_pic_url`; sub-niche-coherent | **GO (logged-out, n=3)** — edge populated logged-out (19 / 32 related accounts for two seeds; `hyram` empty via crawler-strip/opt-out variant). Snowball feasible (`username`+`id` → next wpi). 6 reqs all 200, no 401/429. Residual: snowball depth / coherence / follower-bands / crawler-strip retry / wpi own ceiling = Phase 2. | HIGH ⭐ |
| YouTube long-form + Shorts — 5 creators *(2026-06-21)* | `forseti/product/spines/capture/core/source_families/social_media/youtube/youtube_capture_recon_v0.md` | **Embedded `ytInitialPlayerResponse`** in served HTML (logged-out, no JS): exact `viewCount`/`lengthSeconds`/absolute-ISO `publishDate`/`channelId`/`author`/description. **Comments** via `youtubei/v1/next` panel-scoped continuation — same route both surfaces, paginated, `publishedTime` **relative-only**. | **GO (n=10 logged-out)** — long-form & Shorts share substrate + field paths + comments route → **unified one-runner + `surface_type` switch** (no split trigger fires). Residual: `comments_disabled` posture (NASA), surface_type discriminator = serving-surface not duration, like abbreviated at scale, live/age-restricted/EU-consent unsampled; **capture not yet persisted (recon only)**. | HIGH ⭐ |

**IG reel view/play count (2026-06-14).** Closes part of the prior IG recon's "reel view/play count (in GraphQL JSON, not page DOM)" residual and **refines** its "`web_profile_info` API 429 cookieless → 200 logged-in" line: in a real browser context (IG's `X-IG-App-ID`/web headers) `web_profile_info` returned **200 cookieless** carrying `video_view_count` per media, keyed by `shortcode`; the earlier 429 was the **header-less `direct_http`** rung, not a browser-context XHR. The signal lives in the **profile feed**, not the reel page, so a build folds into the **existing logged-out grid load** — not a per-reel or session capture. **IG reel view/play count — corrected (2026-06-14).** First reported "walls early" from a UI-scroll probe; that was an **artifact** (a DOM login-heuristic that fired regardless of auth, and `mouse.wheel` never triggering IG's infinite-scroll — identical logged-out/session results were the tell — recon **Pattern 1**). The valid method, **following the grid's own `end_cursor` via the `graphql/query`**, paginated **25 pages all `200`, 365 media back to 2017-08-22**, **logged-out**, no wall / no `429`; the **session run was byte-identical** → session buys nothing. Net: `video_view_count` is reachable **logged-out incl. deep history**; the session lane is **retired** for this purpose. **One residual:** sustained cadence at scale (H5 / multi-account-over-time).

**IG creator discovery — suggested-accounts edge (2026-06-15).** Discovery mechanism 1 (the
rising-creator spine) for the IG creator-momentum pipeline is **GO logged-out**: the
related-accounts graph is `data.user.edge_related_profiles` in `web_profile_info` — the **same
tolerant 200-cookieless surface** as calls/stats/reel-views — so the whole pipeline runs on
**one IG substrate**, no off-IG discovery DB and no session. Populated logged-out (19 and 32
related accounts for two seeds; **sub-niche-coherent** — a fragrance seed returns fragrance
accounts), each node carrying `username`+`id` so the **snowball is feasible**. One empty seed
(`hyram`) coincided with the **crawler-strip / login-wall variant** (bundle flag
`should_remove_related_profiles_for_crawlers`) or an account opt-out — a known empties source
for Phase 2 to detect-and-retry, **not** a reachability failure. **Phase 2 (bounded snowball,
2026-06-15): GO mechanics, two design requirements.** Pure-wpi (no profile nav) sidesteps the
strip; 15 reads all 200 (wpi ceiling ≥15); 15 fetches → **243 unique accounts**, 69 multi-set →
bounded community. But (a) **sub-niche coherence degrades at depth** via bridge nodes (one
`@Bible` relation injected a religious cluster) → a **sub-niche filter is now GATING**, not
polish; and (b) a **mega seed surfaces only mid-tier** (≥184k), so the rising tier (~10k–100k)
needs deeper snowball. Production at-scale + the discovery-read posture remain open.
`ig_creator_discovery_suggested_accounts_recon_v0.md` is the finding;
`ig_creator_discovery_spec_v0.md` is the capability spec.

## Coverage map

- **Well-covered:** forums/threads (Reddit ×4, WSO), pricing (M&I, Teal, OpenAI-lane), archive/history (Daimler, Unity), docs-PDF body (Daimler — the strongest anti-bot escalation case), browser runner (CloakBrowser), reviews (ClickUp + Sephora-pending).
- **Thin / single-fixture:** docs-changelog (Kubernetes only), reviews (one merged fixture; the strong one is worktree-pending), SPA embedded-state (Ulta worktree-pending only).
- **ABSENT / PARTIAL — directly relevant to the stated multi-source product direction:**
  **TikTok has no technical recon at all.** **YouTube is now probed** (2026-06-21 — **GO**,
  n=10 logged-out; long-form + Shorts unified, served-HTML embedded state + `youtubei` comments;
  see the Social networks table). **Instagram is now probed** (own-account
  wind-caller recon, 2026-06-14 — **GO demonstrated** at the attended logged-in browser rung;
  see the Social networks table). The only other social probe is the LinkedIn *policy*
  boundary. Any TikTok recipe card is **speculative** until probed; social surfaces carry the
  heaviest ToS/auth-wall/anti-bot posture (entitlement gate, Pattern 4, applies before any
  technical attempt). No media/video capture recipe exists either. (IG media/video capture is
  likewise still unprobed — the IG recon covered caption text + stats, not media bytes.)

## Pending-merge / external (not on main; include before the doctrine finalizes)

- **Sephora/Bazaarvoice reviews finding** — worktree `orca-cloak-scroll-wt`, in squash `0faf262`, force-push pending. The single best **reviews** diagnosis (and the canonical "blocked was wrong" lesson).
- **Ulta Apollo embedded-JSON (DP-002)** — demand-projection lane worktree, unmerged. The single best **SPA-embedded-state** diagnosis.
- **OpenAI price payload (rung-1.5)** — `orca-rung15-wt`, unmerged. Best **pricing-embedded** diagnosis.
- **Operator-supplied / gitignored scratch** (evidence, not tracked): `docs/_inbox/data_capture_pressure_test_operator_supplied_2026_05_29/...`; `forseti-harness/_test_runs/{cloakbrowser_api_probe,source_quality_slot3_*}/`.

## Non-claims

Not an authorization, not a build spec, not validation/readiness/acceptance, not legal
advice. Verdicts are as reported by each source doc. The absence of a TikTok/IG probe is a
**sweep result** (no such recon surfaced across the main-tree docs), not a proof that none
could exist. Worktree-resident findings are **claimed by their lanes** and unverified here
until merged.
