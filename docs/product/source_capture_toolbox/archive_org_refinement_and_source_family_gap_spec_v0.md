```yaml
retrieval_header_version: 1
artifact_role: Capture-spine spec draft (non-authorizing) — archive_org adapter refinements + source-family gap specs
scope: >
  Spec drafts (problem / goal / proposed shape / non-goals / acceptance) for the archive_org
  adapter refinements (date-bound CDX, trajectory capture, URL-form sweep, cross-archive fallback
  ladder, body-retrieve escalation, body verification, source-quality admission gate) and the source-family gaps (LinkedIn forward trend, exec moves, Companies House,
  demand-side signals) surfaced by the org-motion Beauty Pie backtest pilot and the 2026-06-14
  backtest/MGT robustness pass. Spec only — no implementation, no change to existing
  adapter behavior until a separate authorized build turn. Each gap carries its entitlement and
  cross-lane-ownership boundary.
use_when:
  - The capture-spine lane opens a build turn for any archive_org refinement or source-family adapter below.
  - The org-motion / judgment lane needs the capture-side seam + entitlement posture for these signals.
authority_boundary: retrieval_only
open_next:
  - docs/product/source_capture_toolbox/source_capture_playbook_v0.md
  - docs/decisions/source_capture_archive_snapshot_typed_timing_decision_v0.md # nonresolving: pending on unmerged lane
stale_if:
  - The archive_org adapter changes build_cdx_availability_url / select_snapshot signatures.
  - The owner changes the capture risk posture (entitlement hard line) these specs hold.
  - A build turn lands any item below (move that item from spec to its decision record).
```

# archive_org Refinements + Source-Family Gap Specs (v0)

## Provenance and return lane

Couriered from the **judgment lane** (org-motion Beauty Pie backtest pilot, batch-1 case #3),
2026-06-11, which exercised the archive.org path by hand and surfaced these gaps. This doc is the
capture-spine **spec-draft** reply; **it returns to the judgment lane**. Spec only — preserves
existing `archive_org` behavior; no implementation until a separate authorized build turn.

## Hygiene check (asked first by the commission) — RESOLVED

**Canonical playbook = `docs/product/source_capture_toolbox/source_capture_playbook_v0.md`.**
Verified against primary source (directory listing, 2026-06-11): `source_capture_playbook_v0.md`
exists; **`capture_investigation_playbook_v0.md` no longer exists on disk** — it was the
pre-rename name (capture_investigation → capture_runner → source_capture) and is retired. Any
remaining reference to `capture_investigation_playbook_v0.md` is stale and should be repointed.
(Known loose end, capture-spine-owned: the canonical file's internal H1 still reads
"Capture-Investigation Playbook" — title-only drift, not a content fork.)

## Guardrails honored throughout

Public content only · never defeat an auth/access-control gate · market-level signal only, no
individual dossiers. Where a commissioned signal lives behind one of those lines, the spec says
**NO-GO/CATALOG_GAP under posture** and names the forward-commercial path — it does **not** spec a
gate-defeat. This aligns with the owner's affirmed sequence: *get proof → get commercial → invest
in the vendor's product, the vendor bears the ToS* (moat = judgment + cleaning, not a capture farm).

## Prioritization (capture-spine call — commission delegated this)

1. **A — date-bound CDX** — cheapest, code-anchored, removes a live latency/timeout footgun, and unblocks B.
2. **Companies House adapter** — cleanest GO (official free API, no entitlement risk); serves *both* ≤cutoff financial context and outcome verification.
3. **B — trajectory capture** — the core org-motion-trend enabler; depends on A; reuses the just-landed `archive_snapshot_time` typed timing field.
4. **D — URL-form sweep** — removes false NO-GOs; medium effort.
5. **LinkedIn public-surface trend sentinel** — entitlement-bounded; pre-commercial bridge only.
6. **Demand-side signals** — *cross-lane handoff to the demand spine*, not a capture-spine build (see item).
7. **Exec moves / departures** — mostly NO-GO under posture; public-proxy only; lowest capture-spine value.

*Added 2026-06-14 (backtest/MGT robustness pass):* **E — historical cross-archive fallback ladder** —
the single biggest historical-capture robustness lever (removes the single-archive
single-point-of-failure); slots with A/B/D as the archive_org refinement set. Build-order against
A–D is owner / taxonomy-adjudication-dependent (the capture build-order join point: org-motion +
web wind-callers lead under the current default). **F — body-retrieve escalation (probe-then-pin)**
is slice E's retrieve-arm: reuse the existing rungs (incl. the Reddit-proven cloakbrowser), probe
once for the cheapest working rung per archive, then fetch direct at the pinned rung. **G — body
verification** gates F's "usable body" on the *served* snapshot timestamp ≤ cutoff (closing a
body-level no-lookahead leak Wayback redirects can open), URL identity, and content integrity. **H — source-quality admission
gate** computes + enforces the capture-time quality floor from E/F/G's verdicts so a PARTIAL /
G-rejected packet can't pass downstream as decision-grade (fixture-admission / Judgment stay
downstream-owned).

---

## Part 1 — archive_org adapter + playbook refinements

### A. Date-bound the CDX availability query
- **Problem (code-verified):** `build_cdx_availability_url` (`orca-harness/source_capture/adapters/archive_org.py:114-128`) issues the CDX query with only `url/output/fl/collapse` — **no `&from=`/`&to=`**. `select_snapshot` (:149-161) filters `snapshot.timestamp <= cutoff_timestamp` **client-side** after `parse_availability_snapshots` has parsed *every* returned row. On a heavily-archived URL this pulls the full snapshot history each call → latency/timeout, and contradicts the discovery note's own "date-bound the CDX query" lesson.
- **Goal:** accept an optional date window and apply `&from=`/`&to=` (Wayback 14-digit form) on the CDX call; **keep** the `<=cutoff` client-side selection as the anti-leakage guarantee. Defense-in-depth: server-side window for cost, client-side `<=cutoff` for correctness.
- **Proposed shape:** add `from_timestamp` / `to_timestamp` (or a `window` tuple) to `fetch_archive_org_capture` + `build_cdx_availability_url`; when a `cutoff_timestamp` is supplied, default `to` = cutoff (never widen past cutoff server-side), leave `from` operator-supplied/None; validate via the existing `_validate_wayback_timestamp`.
- **Non-goals:** no change to `select_snapshot`'s `<=cutoff` rule (it stays the leak guard); no body-fetch-path change; no caching.
- **Acceptance:** CDX URL carries `from`/`to` when a window is given; a heavily-archived fixture returns within budget; the `<=cutoff` guard still excludes a post-cutoff snapshot even when the server window is wider; absent window → behavior byte-identical to today.

### B. First-class trajectory / time-series capture
- **Problem:** `select_snapshot` returns **one** snapshot (`max(eligible)`) and `fetch_archive_org_capture` fetches one body. A trend (org-motion hiring/headcount) needs a *series*; today that is N manual runs at N cutoffs.
- **Goal:** a trajectory mode capturing N snapshots across a date range at intervals into **one bundled receipt**, `<=cutoff` guard preserved **per snapshot**; at minimum, a documented helper + receipt shape for the N-run pattern.
- **Proposed shape:** `select_snapshot_series(snapshots, *, interval, from, to)` buckets the already-parsed list into intervals and selects one-per-bucket (max within bucket, each `<=` its bucket cutoff); `fetch_archive_org_trajectory` fetches each selected body and emits a bundled result (per-snapshot bodies + a manifest of selected timestamps + per-snapshot timing). **Reuses the typed `archive_snapshot_time` field** from the two-date timing contract (orca#24) for each series member, so each member dates to its own snapshot time, not fetch time.
- **Non-goals:** no scheduler/standing job; no new network behavior beyond N direct-HTTP body fetches (same rung); **no differencing/curve math** — that is the demand-projection consumer's job.
- **Acceptance:** a multi-snapshot fixture yields one bundled receipt with K members at the requested intervals; each member's selected timestamp `<=` its bucket cutoff; the single-snapshot path is unchanged.

### D. URL-form sweep before concluding "no coverage"
- **Problem:** archive coverage is URL-form-sensitive. Gate-0 evidence: `uk.linkedin.com/company/…` held a pre-cutoff snapshot the bare/`www` hosts did not; trailing-slash and `boards.eu` vs `boards` also flip results. Today `parse_availability_snapshots`→`[]`→`select_snapshot`→`None` returns NO_SNAPSHOTS on the *first* form, with no variant retry.
- **Goal:** a bounded variant-sweep (host/path forms) before returning NO_SNAPSHOTS, with the tried variants recorded in the receipt.
- **Proposed shape:** `url_form_variants(original_url)` generates a *capped* set (host: bare ↔ `www` ↔ known cc-subdomains e.g. `uk.`; path: trailing-slash on/off) feeding an ordered CDX sweep that stops at the first form with a pre-cutoff snapshot; record `variants_tried` + `variant_selected` in the availability metadata.
- **Non-goals:** no semantic URL rewriting; **no unbounded subdomain enumeration**; no change to selection once a form hits; a found snapshot remains subject to the entitlement gate (Part 2).
- **Acceptance:** a fixture where only `uk.` holds a pre-cutoff memento now returns it; `variants_tried` recorded; a truly-absent URL still returns an honest NO_SNAPSHOTS *after* the bounded sweep.

### E. Historical cross-archive fallback ladder
- *Provenance:* added 2026-06-14 by the capture-spine backtest/MGT robustness pass (not the 2026-06-11 Beauty Pie courier). Verified against source this pass: the originally-sketched "Memento aggregator" rung is **dead** — `timetravel.mementoweb.org` was taken down end-2025 (static info page only in 2026); the LANL aggregator is open-source but self-hosting it is standing infrastructure (MGT-rejected). archive.today exposes a Memento API (since 2013) but carries an intermittent reachability caveat (Cloudflare-1.1.1.1 / EDNS DNS conflict + anti-bot, unresolved as of 2025-10).
- **Problem (code-verified):** `fetch_archive_org_capture` (`orca-harness/source_capture/adapters/archive_org.py:60`) queries **only** Wayback (`DEFAULT_CDX_ENDPOINT`). On a Wayback miss (`select_snapshot`→`None`) or body-fail (`body_result` failure) it returns NO_SNAPSHOTS/PARTIAL with **no escalation to any other archive**. The Daimler pre-cutoff NO-GO is honest precisely because only one archive was asked — so a backtest's historical capture is a single-archive single-point-of-failure.
- **Goal:** a bounded, cheapest-first **cross-archive LOCATE ladder** — on a Wayback miss/body-fail, query a small fixed ordered set of independent archives' *own* Memento endpoints (NOT a self-hosted aggregator), preserve the per-archive `<=cutoff` leak-guard, route the located memento's body through the live rung ladder (slice F), and keep NO-GO/PARTIAL first-class. It separates the two orthogonal axes the playbook already names: **locate** (does a pre-cutoff memento exist anywhere — slice E) vs **retrieve** (can the body be fetched — slice F). *MGT framing:* most of an aggregator's cross-archive value at a fraction of cost (no standing service); **named limitation — a small maintained archive list, not auto-discovery of all ~20 archives.**
- **Proposed shape:** a thin `fetch_historical_capture` orchestrator **above** per-archive adapters (NOT inside `archive_org.py`, which stays the Wayback rung — this keeps each archive's parsers isolated, matching the one-adapter-per-source-family pattern). Ordered locate set: (1) **Wayback CDX** (reuse `archive_org.py`, primary); (2) **`archive_today` adapter** (new; its own Memento TimeGate/TimeMap; reachability caveat → body via the rung ladder; no-gate-defeat — CAPTCHA / Cloudflare-challenge-solving = stop, not solve); (3) **publisher version-history** (conditional, only when the source *is* a doc/wiki: MediaWiki page-history API, GitHub commit history — ground-truth, free, N/A for most brand/retailer pages). Each rung: query availability `<=cutoff`, select the latest pre-cutoff memento, hand its URL to the body-retrieve step (slice F), stop at the first retrieved pre-cutoff body. Bundled receipt: `archives_tried` (ordered; per-archive availability outcome + `<=cutoff` evidence), `archive_selected`, `body_rung_used`.
- **Non-goals:** no self-hosted aggregator / no standing crawler (rejected maximal); **`timetravel.mementoweb.org` is not a dependency anywhere** (verified dead); no Common Crawl bulk pipeline (per-URL CDX is a *named-deferred* deep rung, not in the default ladder); no gate-defeat; no change to the per-archive `<=cutoff` leak-guard; body-retrieve escalation is **slice F** (referenced, not redefined here); no unbounded archive/URL enumeration (fixed list; URL-form variants bounded per slice D).
- **Acceptance:** (a) **v1 (Wayback + publisher-history, per (b+)):** a fixture where Wayback has no pre-cutoff memento but the source is a doc/wiki with publisher-history → the ladder locates + retrieves it; `archives_tried` records the Wayback miss then the publisher-history hit. **(a, fast-follow):** the archive.today variant (Wayback miss → archive.today hit, `archive_selected = archive_today`) lands with the archive.today rung post-probe, not in v1; (b) an all-miss fixture → honest NO-GO after the bounded ladder, each miss recorded; (c) the per-archive `<=cutoff` guard excludes a post-cutoff memento on any archive; (d) the single-archive Wayback-hit path is byte-identical to today (no regression); (e) `timetravel.mementoweb.org` is not referenced anywhere.
- **Owner-deferrable + MGT-honesty (AR-03):** whether archive.today is a **required** second general archive rung for v1, or deferred. Named honestly: "degrades gracefully to Wayback + publisher-history" holds **only for sources that have publisher history** (docs/wiki/GitHub); for **ordinary brand/retailer pages** (the motivating backtest case) publisher-history is N/A, so deferring archive.today leaves **Wayback-only — the single-archive SPOF is preserved, not removed**. So either (a) archive.today is **required** for v1, or (b) v1 ships as the narrower **"Wayback + publisher-history-only"** variant **explicitly labeled as not removing the SPOF for ordinary pages**, with acceptance and the MGT limitation downgraded accordingly. **Owner decision (2026-06-14): (b+)** — v1 ships **Wayback + publisher-history**, explicitly labeled as not removing the SPOF for ordinary brand/retailer pages; **archive.today is a committed fast-follow** (next slice) gated on its AR-02 served-time + no-gate-defeat reachability probe; **Common Crawl per-URL CDX is the backup** second general rung if archive.today fails the gate. Not deferred-and-forgotten — the SPOF for ordinary pages closes in the fast-follow.

### F. Body-retrieve escalation — probe-then-pin
- *Provenance:* added 2026-06-14, same backtest/MGT robustness pass; the **retrieve-arm** of slice E (E locates a memento; F fetches its body). Shape set by owner 2026-06-14: **do not run a full escalation ladder on every fetch** — probe once to find the cheapest working rung per archive/source, pin it, then fetch direct at the pinned rung; re-probe only when the pinned rung fails. The ladder is a discovery tool, not a per-fetch runtime cost.
- **Problem (code-verified):** archived-body retrieval is locked to one rung — `fetch_archive_org_capture` calls `fetch_direct_http_capture` on the snapshot URL (`orca-harness/source_capture/adapters/archive_org.py:107`) and on failure returns PARTIAL with **no escalation**. archive.today bodies (behind Cloudflare/anti-bot) and rate-limited Wayback (HTTP 429 — Wayback is *not* Cloudflare-fronted; it simply throttles under load) therefore read as NO-GO/PARTIAL when a higher rung would succeed — contradicting "blocked is a hypothesis" and the Daimler escalation evidence.
- **Goal:** a body-retrieve dispatcher with two modes — **probe** (escalate cheapest-first through the existing live rungs to *discover* the working rung) and **steady-state** (fetch direct at the *pinned* rung, no re-escalation). Reuses the existing adapters; preserves availability≠body and NO-GO/PARTIAL.
- **Proposed shape:** `retrieve_body(url, *, pinned_rung=None, max_rung, cutoff_context)`. No `pinned_rung` → **probe**: escalate direct-HTTP → anti-blocking-HTTP → headless browser → **cloakbrowser+proxy** (the same `cloakbrowser_snapshot.py` machinery the Reddit screening-read route already uses against Reddit anti-bot), stop at the first usable body, return `body_rung_used`. With `pinned_rung` → **steady-state**: fetch direct at that rung; **on failure — where failure = any *non-usable* result, not just transport (AR-05): a slice-G verification failure (served-time / identity / content-integrity), an H sub-floor status when H is available, as well as transport / non-2xx / empty — re-probe** (escalate from the pinned rung), and record `pin_reused` / `pin_reprobe_reason` / `pin_replaced_by` in the receipt. The caller **records the working rung per archive / source-family** — the capture-recon-index already records cheapest-GO-rung per source, so the pin reuses that pattern (no new state store; build turn decides doc-vs-runtime record). The slice-E orchestrator calls this per located memento.
- **Stop conditions:** first usable body (2xx, non-empty, passes slice-G verification) | **gate-defeat line** (auth wall / CAPTCHA / Cloudflare *challenge* → STOP, do not solve) | ladder exhausted → honest PARTIAL.
- **Non-goals:** no gate-defeat (challenge-solving is a hard stop); **no full escalation ladder on every fetch** (probe-then-pin); **no refactor of `archive_org.py`'s existing direct-HTTP body path** (additive dispatcher; rung-1 fold-in deferred); no new fetch engines (reuse `direct_http` / `anti_blocking_http` / `browser_snapshot` / `cloakbrowser_snapshot`); no change to the `<=cutoff` leak-guard (slice E owns locate).
- **Acceptance:** (a) probe on a memento whose direct-HTTP 403s but renders at the browser/cloakbrowser rung → returns the body with `body_rung_used` recorded; (b) steady-state with a pinned rung fetches direct at that rung without re-walking cheaper rungs; (c) a pinned rung that starts failing triggers a re-probe; (d) a Cloudflare *challenge*-only memento → STOP at the gate-defeat boundary (PARTIAL), not a solved challenge; (e) ladder exhausted → honest availability≠body PARTIAL with the escalation trail; (f) the existing single-rung `archive_org.py` path is unchanged when the dispatcher isn't invoked.

### G. Body verification — served-time cutoff + identity + content integrity
- *Provenance:* added 2026-06-14, same backtest/MGT robustness pass; the integrity gate slices E/F lean on ("usable body"). The centerpiece is a no-lookahead integrity hole, not just content hygiene. Fixed 2026-06-14 (owner-agreed): per-archive cutoff check + E↔G re-pick, after a live Wayback probe confirmed the leak.
- **Problem (code-verified):** `fetch_archive_org_capture` records `body_result` (`orca-harness/source_capture/adapters/archive_org.py:105`) but never verifies the *delivered* body. Three silent-pass holes: (1) **served-time cutoff leak** — Wayback can 302 to the *nearest* available capture, which may be **post-cutoff**, defeating `select_snapshot`'s selection-time `<=cutoff` guard at the body level (select `20230912`, replay serves `20231002`); (2) **soft-404** — an archive "not archived / not found" page served with HTTP 200 + non-empty body; (3) **charset garble / identity drift** — wrong-encoding decode, or a served original-URL that differs from the requested one (cf. the archive_org adversarial review's A-05 provenance-imprecision finding).
- **Goal:** a body-verification check that gates slice-F's "usable body" on **(1) cutoff integrity** — the *served* snapshot timestamp `<= cutoff` (closes the body-level no-lookahead leak); **(2) identity** — served original URL matches requested; **(3) content integrity** — not a soft-404/placeholder, not charset-garbled/empty-after-strip. On any fail → PARTIAL (availability≠body), never silent-pass; record the verdict in the receipt.
- **Proposed shape:** `verify_archive_body(result, *, requested_url, requested_timestamp, cutoff)` returns the verdict the slice-F dispatcher consumes as its "usable body" gate. The cutoff check carries an **archive-specific served-time proof contract** (AR-02) — per rung, name the trusted metadata source, parser expectation, and missing/unparseable behavior (→ verification failure or explicit rung deferral, **never silent pass**). **Wayback**: `Memento-Datetime` (**observed** — see below) → assert `served_ts <= cutoff`. **archive.today**: *expected* to expose it per the Memento standard but **unproven here** → behind a pre-build assumption probe (build-verify its served-date header; until proven, missing served-time is a verification failure, not an assumed pass). **publisher-history**: bind the *requested revision's timestamp + identity* (not an opaque revision id alone). Also assert URL-identity match and content-integrity markers (archive not-found placeholder detection; decode/charset sanity). **On a post-cutoff served date, do not just NO-GO — signal slice E to re-select the next-older pre-cutoff snapshot** (E↔G loop); reach NO-GO only when no pre-cutoff snapshot yields a clean body. Reuses the existing limitation-note machinery.
- **Finite candidate cursor (AR-01 — E↔G):** the per-archive temporal candidate sequence is a **bounded, receipt-visible cursor** — candidates ordered newest-pre-cutoff-first, each tried at most once (duplicate-detected), each rejection recorded (`snapshot_id` + reason + served-ts when available); an archive rung is **exhausted** when its bounded candidate list is consumed, then the ladder advances to the next archive, reaching NO-GO/PARTIAL only when **all** archives' cursors are exhausted. The receipt must prove exhaustion so "no pre-cutoff snapshot yields a clean body" is auditable (per the playbook receipt contract).
- **Non-goals:** no semantic/meaning validation; **no change to `select_snapshot`'s selection-time `<=cutoff` guard** (G adds the *served-time* check the selection guard structurally cannot see); body fetch + escalation is slice F.
- **Acceptance:** (a) a Wayback body that redirects to a **post-cutoff** snapshot → verification rejects it as a cutoff leak **and signals slice E to re-pick the next-older pre-cutoff snapshot** (NO-GO only when none yields a clean body); (b) a soft-404 "not archived" HTTP-200 page → flagged not-usable → PARTIAL; (c) a charset-garbled body → flagged not-usable; (d) a clean body whose served timestamp `<= cutoff` and URL matches → passes; (e) a body-verification verdict is recorded in the receipt for every retrieved body.
- **Observed (2026-06-14 live Wayback probe — leak is real, not assumed):** a request for `…/20230920120000/…` `302`'d to `…/20230920114426/…` (requested ≠ served) and the `200` carried `memento-datetime` + `x-archive-orig-date`; and the leak reproduced — a request for `…/20230101000000/…` (imagine cutoff 2023-01-01) was served the `20230912135629` capture, i.e. a **post-cutoff body for a pre-cutoff request**. So the served-date check is implementable against a real header for Memento archives; publisher-history uses revision-id identity (no Memento header).

### H. Source-quality admission gate
- *Provenance:* added 2026-06-14, same backtest/MGT robustness pass; the **closer** — it consumes E/F/G's verdicts. Enforcement-placement lens (distillation/EP doctrine): the mechanical floor is code-enforceable at the capture→Judgment boundary; the "good enough for THIS decision" judgment stays actor-carried downstream.
- **Problem:** the source-quality tokens (`mini_god_tier_met`, `mini_god_tier_with_visible_limitations`, `archive_body_not_preserved`, `body_possession_not_proven`, lifecycle `scratch/candidate/recommended/separately_admitted`) are **post-hoc doc classifications** in `source_quality_mini_god_tier_profile_v0.md`, not computed/enforced at capture time. So a PARTIAL (availability≠body), a slice-G-rejected body (cutoff-leak / soft-404 / garble), or a NO-GO-after-ladder result can flow downstream **without its quality verdict gating it** — a sub-threshold capture gets silently treated as decision-grade.
- **Goal:** a capture-time admission gate that (1) **computes** the source-quality token from the packet's E/F/G evidence (selected archive, body-rung, body-verification verdict, availability-vs-body) against the profile's six criteria, and (2) **enforces a mechanical floor** — a packet that is body-not-preserved, slice-G-rejected, or NO-GO-after-ladder **cannot be marked decision-grade** (`mini_god_tier_met` / `recommended`); it is capped at `*_with_visible_limitations` / `archive_body_not_preserved` / `scratch`, with the limitation tokens travelling forward so downstream sees them.
- **Proposed shape:** at `node:capture-packet-emit`, derive the source-quality token from the packet's E/F/G evidence + the six criteria; a **deterministic floor** (code-enforced — a packet-emit contract assertion, EP-clean) blocks decision-grade status when body/verification/availability evidence is sub-floor; the limitation tokens are written into the packet. **Negative-only automation (AR-04):** capture-time automation is limited to **evidence emission, limitation propagation, and negative / sub-floor caps**; a **positive** token (`mini_god_tier_met` / `recommended` / `separately_admitted` / decision-grade) is **never auto-finalized** at emit — it stays operator / separate-decision, marked `operator_review_required` (the state assembler already forbids automated `mini_god_tier_met`). A deterministic negative cap is safe; deterministic positive finalization is not. The "is this quality sufficient for THIS decision" call stays actor-carried in the downstream lane.
- **Non-goals:** **no fixture admission** (stays the separate downstream decision — the `needs_separate_fixture_admission_decision` token); **no Judgment scoring / no ECR schema**; no change to the profile's token definitions (slice H consumes them); does not re-decide E/F/G (consumes their verdicts). Build-verify the boundary against `source_quality_state_assembler_v0.md` + `source_capture_packet_fixture_admission_criteria_v0.md` so the gate enforces the capture-side floor without encroaching on fixture-admission / Judgment ownership.
- **Acceptance:** (a) a body-not-preserved packet cannot be emitted as `mini_god_tier_met` / decision-grade — capped + limitation carried; (b) a slice-G-rejected (cutoff-leak) body → packet marked PARTIAL / not-decision-grade, never clean; (c) a clean GO packet (body preserved, G-passed) → eligible for decision-grade (subject to the downstream fixture/Judgment decisions); (d) the computed token + limitations are recorded in the packet for every emit; (e) downstream fixture-admission / Judgment ownership is unchanged; (f) **no positive token** (`mini_god_tier_met` / `recommended` / `separately_admitted`) is auto-finalized at emit — positive finalization carries `operator_review_required` and stays operator / separate-decision.
- **Owner-check:** slice H sits at the capture↔Judgment seam — confirm the capture-side floor doesn't overlap the existing fixture-admission / JSG gate ownership (it computes + enforces the capture quality floor; it does not admit to fixtures or score).

---

## Part 2 — source-family gaps (capture seam + entitlement + ownership)

### LinkedIn headcount / follower TREND (forward / live company page)
- **Problem:** not archive-backtestable (Wayback didn't capture mid-size company pages pre-2025) — the missing second org-motion leg.
- **Goal:** forward/live public company-page capture (size band, `numberOfEmployees`, follower count) building a go-forward trend; **market-level only, no individual dossiers**.
- **Proposed shape:** a forward sentinel reading the **public logged-out** company page (size band / follower count are visible there) at human rate, into a trajectory receipt (reuse B's series shape). **Entitlement hard line:** logged-out public fields only; **never** an authenticated read; if the public page gates a field behind login, that field is **NO-GO under posture** (do not defeat the gate). Per proof→commercial→vendor, the durable forward path is a commercial people-data vendor that bears the ToS — the public sentinel is the **pre-commercial bridge only**.
- **Non-goals:** no auth; no per-person tracking; no employee-list scraping.
- **Acceptance:** public size-band + follower count captured logged-out into a dated series; any login-gated field recorded as entitlement-NO-GO, not captured.
- **Ownership flag:** trend math/consumption is the org-motion/judgment lane's; capture spine owns only the public-surface read + receipt.

### Senior moves / departures
- **Problem:** behind LinkedIn auth; logged-out archive bytes don't carry it.
- **Goal (as commissioned):** a forward exec-moves signal using **entitled/public access only**.
- **Honest spec answer:** under the entitlement hard line this is largely **NO-GO / CATALOG_GAP for self-capture** — the signal lives behind auth and the posture forbids defeating it. In-posture capture-side options are narrow: **(a)** a public proxy — company "leadership"/team pages + press/PR + Companies House director appointments/terminations (next item); **(b)** a commercial people-moves vendor that bears ToS (forward-commercial path). Spec **(a)** as the public-proxy capture seam; name **(b)** as the forward path. **Do not** spec an authenticated LinkedIn capture.
- **Acceptance:** an exec-move proxy assembled from public filings/PR/leadership pages only; the LinkedIn-auth route explicitly recorded as out-of-posture.
- **Ownership flag:** signal definition is the judgment/org-motion lane's; capture spine holds the line and supplies the public proxy.

### Companies House filings
- **Problem:** a different source-family (structured UK filings) not primed; needed for ≤cutoff financial context **and** outcome verification.
- **Goal:** a CH adapter (accounts / filing history by company number).
- **Proposed shape:** a structured-API adapter against the **official Companies House public API** (free, registration-keyed — entitlement is a *free API key*, not a gate-defeat → clean GO). Methods: filing history + accounts by company number; map the **filing date as a real typed source date** into the packet timing contract (feeds ECR cleanly, exactly like the `archive_snapshot_time` fix). The cleanest GO in Part 2.
- **Non-goals:** no scraping the CH website (use the API); no paid data products.
- **Acceptance:** filings/accounts retrieved by company number via the official API with a key; filing dates typed into the packet; rate/posture documented.
- **Ownership flag:** capture spine owns the adapter; *which* filings matter is the org-motion/judgment lane's.

### Demand-side signals (the demand spine)
- **Problem:** the fusion's other half (search / social / review-velocity / traffic); without it backtests test org-motion against a thin baseline.
- **Goal:** a demand-signal capture.
- **Ownership flag (load-bearing):** this is the **demand-projection / demand-spine lane's** territory — note the active consumer-demand pivot (the wave of `docs/product/product_lead/*` + `*_consumer_demand_*` artifacts now on the branch). Capture spine should **not** design the demand spine's product. Capture-side answer: capture spine supplies the *capture seam* for whichever demand surfaces that lane selects — review-velocity already has recon (Bazaarvoice/Sephora GO; Reddit GO), and the creator-momentum surfaces are catalogued in `docs/research/creator_momentum_data_landscape_v0.md` — reusing the playbook routes. **Demand-signal selection + projection is a cross-lane handoff to the demand spine, not a capture-spine spec.**
- **Acceptance:** capture spine provides per-surface capture recipes on request; demand-signal *definition* deferred to the demand spine.

*(ATS / job-boards intentionally excluded per the commission — built elsewhere.)*

## Non-claims

Spec drafts only — not implementation, not validation, not readiness, not acceptance, not ECR
ratification, not a capture authorization. Code line numbers are evidentiary for the 2026-06-11
read of `archive_org.py` and must be re-verified at build time. Entitlement verdicts (LinkedIn
NO-GO-under-posture; Companies House GO) are posture calls under the current capture risk posture,
not legal advice. Each item moves from spec to its own decision record when a build turn lands it.
