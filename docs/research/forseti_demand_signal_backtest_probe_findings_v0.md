# Forseti Demand-Signal Reconstructability + Backtest Feasibility Probe — Findings v0

```yaml
retrieval_header_version: 1
artifact_role: Research findings report (probe/validation tier; evidence, not product authority)
scope: >
  Findings of the two-part demand-signal probe commissioned by
  docs/workflows/forseti_demand_signal_backtest_probe_handoff_v0.md (PR #832;
  readable from origin/claude/sleipnir-ci-product-shape-ab29bd until that PR
  merges): (1) a reconstructability inventory of public demand signals
  (Class A/B/C per the un-backfillable-signal moat doctrine), and (2) a
  zero-lookahead retrospective feasibility test of reconstructed signal
  series against SEC-filed outcomes for a 5-ticker consumer pilot set
  (ELF, EL, ULTA, CELH, CROX). Everything product_learning-capped.
use_when:
  - Deciding whether to invest in a real (pre-registered, forward) backtest program.
  - Checking which venues/signal classes can be rebuilt zero-lookahead today, at what fidelity.
  - Designing capture priorities informed by observed Class-B decay events.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_unbackfillable_signal_moat_doctrine_v0.md   # taxonomy under test (PR #832; same branch as the packet until merge)
  - docs/workflows/forseti_research_engine_map_v0.md
stale_if:
  - The owner commissions and lands a real forward backtest program (point here to it).
  - The un-backfillable-signal moat doctrine (PR #832) is revised in a way that changes Class A/B/C boundaries.
  - Amazon/Wayback/Wikimedia/Reddit-archive access posture changes materially from the July-2026 state recorded here.
```

## Status and claim tier

`PROBE_FINDINGS_REPORTED`. Probe/validation tier only; `product_learning`-capped.
This is an in-sample, selection-aware feasibility read — **not** a backtest
result, not a hit rate, not a track record, not buyer proof, and not capture
authorization. Retrospective correspondence is backtest fuel; the sellable
record only accrues live and forward (see the moat doctrine, PR #832).

## Provenance

- Commissioned by: `docs/workflows/forseti_demand_signal_backtest_probe_handoff_v0.md` (PR #832,
  packet commit `a40acc1b`, branch `origin/claude/sleipnir-ci-product-shape-ab29bd`;
  packet not yet on `main` at probe time — its `stale_if` pointer update is a
  named follow-up below).
- Executed by: lane `claude/forseti-demand-signal-context-9b1ef6` (worktree off
  `origin/main` @ `668b0e0d`), 2026-07-10. Load contract outcome `REUSE`;
  `SOURCE_CONTEXT_READY` declared after re-reading the packet's named sources.
- Pilot-scope fork: surfaced to owner; packet default adopted (ELF, EL, ULTA
  beauty + CELH, CROX non-beauty). Reversible; owner may redirect.
- Read posture: screening-tier scouting/diagnostic reads only (Walker-kit
  rules: public logged-out pages, human-rate, URLs + dates + short quotes;
  TikTok/IG/LinkedIn pointer-only; no reddit.com fetches). No Source Capture
  Packets were emitted and nothing here enters capture-lane data; per-venue
  route/ToS bindings were not stretched (adjudication needs are named, not
  assumed). EDGAR pulls used the standard public `data.sec.gov` APIs — verified
  during load: no dedicated EDGAR tooling exists in `forseti-harness` today.
- Instrument notes (for re-runners): the agent-side WebFetch tool refuses
  `web.archive.org`; all Wayback CDX/snapshot reads ran via shell HTTP
  (PowerShell `Invoke-RestMethod`/`Invoke-WebRequest`, UA-disclosed, sequential,
  ~2-3s spacing, `id_` raw endpoint). A mid-run account spend limit terminated
  two delegated series builds; they were completed inline (same recipes).

```text
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom (S1 + packet ledger: research-engine map, CSB/Scanning
    READMEs, capture consolidation map, safety-rules, moat doctrine @ PR #832,
    thesis Strategic Center, growth map section E, Walker kit,
    retrieval-metadata, decision-routing, artifact-folders)
  edit_permission: docs-write (lane branch)
  target_scope: this findings report under docs/research/
  dirty_state_checked: yes (clean; lane HEAD == origin/main @ 668b0e0d at start)
  blocked_if_missing: none
```

## Part 1 — Reconstructability inventory (signal class x venue)

Access date for all rows: 2026-07-10. Class labels per the moat doctrine
(PR #832): **A** = un-backfillable point-in-time state (moat-grade only if
captured live); **B** = rebuildable from dated items / archive snapshots
(backtest fuel, NOT moat); **C** = vendor/filed history (ground truth or
convenience, no moat).

| Signal class | Venue/route | Rebuild method today | Class | Fidelity / bias / cost (observed) |
|---|---|---|---|---|
| Reviews w/ dates | Amazon live `/product-reviews/` | none logged-out | — | CLOSED: login-walled since 2024-11, hardened by 2026-05 (fetches 503'd; corroborated by secondary sources). Dated-review pagination is no longer public. |
| Review counters | Amazon PDP via Wayback snapshots | CDX walk -> `id_` snapshot -> `acrCustomerReviewText` extract | B | WORKS for mono-SKU staples: quarterly-or-better snapshot density (CELH variety pack, e.l.f. Power Grip); counter populated in snapshots through at least 2025-06 (CELH) / 2025-03 (ELF); three Nov-Dec 2025 samples had the widget present but EMPTY -> late-2025 render change is closing this window. Biases observed IN THIS PROBE: a review purge (ELF -1,108 ratings Mar-Jun 2024), listing-title drift, and review-pool merges (see CROX/CELH events below). Cost: slow (~20s/snapshot), free. |
| Review counters | Multi-variant apparel PDPs (Crocs) | same | B (fails) | NOT reconstructable at usable fidelity: coverage fragments across color/size ASINs (best candidate: 4 usable snapshots in 5y), and pool identity is unstable — observed re-parent event: 38 ratings (4.1 stars) -> 336,875 (4.8 stars) in 19 days (2022-07-14 -> 2022-08-02, ASIN B09JNKQZ56). Counter series for such products measure LISTING surgery, not demand. |
| Review counters + rank + price, many SKUs | Retailer category/listing pages via Wayback (Ulta `shop/makeup`) | snapshot -> embedded per-tile JSON (`"rating"`, `"reviewCount"`, `"listPrice"`) | B | Richest single source found: near-monthly snapshots 2022-2025 (47/48 months) with structured counters for dozens of SKUs per capture. Untested at extraction scale in this probe (one sampled snapshot verified). |
| Bestseller rank + price | Amazon PDP via Wayback | same as counters | B | Rank + price rendered in ALL sampled snapshots incl. late-2025 (survives the counter-empty change). Sparse/irregular (crawl-cadence artifact). |
| Comments w/ dates | Reddit via Pushshift-lineage (PullPush API `before`/`after`; Arctic Shift; Watchful1 academictorrents monthly dumps 2005-06 -> >=2025-12) | date-bounded query or offline dumps | B | Technically strong: exact timestamps, full 2022-2025 window, monthly-to-daily granularity; dumps are the defensible frozen anchor. BUT the whole lineage is legally contested by Reddit (prior shutdown cycle; adversarial ToS at PullPush) -> **route/ToS adjudication is capture-lane-owned; NOT used for Part-2 scoring in this probe.** Survivorship: ~25% of comments from deleted accounts (primary-verified); archive-completeness gap itself is small (0.043% comments). |
| Subreddit subscriber counts | old.reddit pages via Wayback (archive.org fetches, not reddit.com) | CDX walk -> `<span class="subscribers">` extract | B | Verified parseable (r/Sephora 107,778 readers @2023-05-14; r/energydrinks 69,155 @2023-11-11); ~21 snapshots per subreddit 2022-2025 at 2-4 month spacing -> spot-check anchors only. Dedicated trackers are dead or degraded (frontpagemetrics domain squatted; subredditstats self-reports stale). Brand->subreddit->ticker mapping too indirect for outcome scoring. |
| Posts/videos w/ dates | YouTube | Data API v3 (`publishedAfter/Before`, exact `publishedAt`; free key, ~100 search calls/day) or per-video `datePublished` meta-tag scrape for known IDs | C (API) / B (meta) | Viable-with-key; NOT exercised in this probe (no key provisioned; bare-GET search is JS-walled). Comment dates exact via API only (logged-out UI is relative-only). |
| Point-in-time view counts | YouTube via Wayback / Social Blade | snapshot / vendor | A (mostly) | Effectively un-backfillable: zero snapshots for two mid-tier brand videos tested; Social Blade free tier can't reach 2022-2024 daily, paid capped ~3y (from 2026-07 reaches only ~mid-2023). Survivorship bias toward already-viral content. Confirms the doctrine's Class-A framing empirically. |
| Posts + engagement | TikTok / Instagram | pointer-only (capture-lane-owned) | A | Structurally near-unreconstructable from public archives (JS-walled replay; documented Wayback failures); no open vendor since CrowdTangle shut down 2024-08-14 (replacement is restricted and cannot track performance over time). Historical follower/engagement series exist only where a tracker captured live -> vendor-captured Class A. |
| Search interest | Google Trends | UI/CSV export, no official API | C | Retrievable but NOT stable: fresh random sample + 0-100 re-normalization per pull -> two researchers pulling the "same" 2022-2025 window on different days get different series. Usable as coarse context, weak as scoring input. |
| Attention proxy | Wikipedia pageviews (Wikimedia REST API + raw dumps since 2015) | one API call per article/month range | C (frozen) | Cleanest zero-lookahead series found: exact timestamps, free, immutable once published, independently rebuildable from raw dumps. Two REAL failure modes observed in this probe: article-age truncation (Celsius Holdings article has data only from 2024-02) and title-rename fragmentation (the e.l.f. article moved E.l.f. Cosmetics -> Elf (cosmetics) -> E.l.f. (cosmetics) -> E.l.f. in 2024-09; pageview history does NOT follow renames and had to be stitched via the move log). Measures curiosity/news attention, not purchase intent. |
| App downloads / web traffic | Sensor Tower (abs. data.ai), Appfigures, Similarweb | licensed only | C | Dead ends for a screening probe: historical series are paid/enterprise; free tiers are snapshots. Vendor-modeled estimates, not counts. |
| Filed outcomes | SEC EDGAR (`data.sec.gov` companyfacts + submissions APIs) | public JSON APIs | C | Fully rebuildable ground truth: quarterly revenue + filing dates + 8-K dates built for all 5 tickers with zero gaps. Caveats: Q4 must be derived (FY minus Q1-Q3) for EL/ULTA/CELH/CROX (no discrete Q4 filed); XBRL tag drift (CELH dual-tagged; ULTA uses legacy `Revenues`). |

**Part-1 verdicts.**
1. Class B is real but *decaying and bias-laden*: this probe directly observed a
   venue closing (Amazon dated reviews), a counter de-rendering (late-2025
   snapshots), a purge, two pool-identity events, an article-age truncation, and
   a rename fragmentation. What is reconstructable today was more reconstructable
   yesterday — which is itself evidence for the capture-forward (Class-A) moat
   thesis: nothing below Class A stays rebuildable on demand.
2. Reconstruction quality is *product-structure-dependent*: mono-SKU staples
   (energy drinks, hero cosmetics) rebuild well; multi-variant apparel does not.
3. The strongest untapped Class-B lode is retailer listing pages with embedded
   structured JSON (Ulta-style): many SKUs per snapshot, near-monthly cadence.
4. The strongest dated-item stream (Reddit) is gated on a capture-lane ToS
   adjudication, not on technique.

## Part 2 — Zero-lookahead backtest feasibility

### Pre-registration and deviations

The cutoff design, quarter-selection rule, scoring buckets, and series
candidates were fixed in writing before any signal series was assembled, and
amended once (additive, disclosed, before any signal read) after Part-1
instrument findings showed the original quarter rule would concentrate scoring
where the Wayback counter window was likely closed. Summary of the
pre-registered design (full text preserved in the lane scratchpad and
reproduced in the recipes below):

- Cutoff per (ticker, quarter) = fiscal `period_end` from EDGAR; every series
  item must carry a verifiable timestamp <= cutoff (the print lands weeks
  later, so cutoff < filing date always; snapshot capture timestamps and
  API-served month stamps are the timestamp sources).
- Quarters per deep ticker (ELF, CELH, CROX): steepest YoY-revenue-growth
  change pair overall + steepest pair within 2022-2023; light tickers
  (EL, ULTA): 2 most recent filed quarters, S2 only. Quarter selection is
  outcome-aware by construction — DISCLOSED BIAS; this is a feasibility read,
  not a hit rate.
- signal_read in {accelerating, steady, decelerating, too_thin}; outcome_read
  from YoY growth delta at 2pp threshold; correspondence in
  {MATCH, adjacent, MISS, too_thin}; too_thin if <3 usable points <= cutoff or
  a coverage gap crosses the window.
- Series candidates: S1 Wayback Amazon ratings velocity; S2 Wikipedia
  pageviews; S3 Reddit mentions — **dropped before scoring** (route/ToS
  adjudication is capture-lane-owned; Drift Guard forbids per-task stretching);
  S4 YouTube uploads — **dropped before scoring** (viable only via keyed API;
  no key provisioned in this probe).

### Series build receipts (zero-lookahead hygiene)

**S1 ELF** — e.l.f. Power Grip Primer, ASIN B09XMYFTB7 (10 snapshots,
2022-10-21 -> 2025-03-21; delegated build, completed pre-spend-limit).
Timestamps = Wayback capture times; snapshots selected nearest quarter
boundaries; genuine archive gaps: Q1-Q3'22 (only bot-shell captures exist) and
Q3-Q4'24 (sub-3KB captures only). Anomaly: cumulative count FELL 21,764 ->
20,656 between 2024-03-01 and 2024-06-02 (purge; recorded as-is).
Series (ts | cumulative ratings | stars): 20221021 2,010 4.6 · 20230326 5,616
4.6 · 20230601 8,187 4.6 · 20231021 16,234 4.6 · 20231207 17,848 4.6 ·
20240301 21,764 4.6 · 20240602 20,656 4.6 · 20240808 22,765 4.6 · 20250115
26,404 4.6 · 20250321 28,291 4.6. Exact per-row `id_` URLs preserved in the
delegated build return (lane transcript) and re-derivable from the CDX recipe
below (`matchType=prefix` variant needed — affiliate-tagged captures carry the
density).

**S1 CELH** — CELSIUS Variety Pack, ASIN B06X6J5266 (8 snapshots, 2021-11-24 ->
2025-06-12; built inline after the delegated build was terminated by the spend
limit). Identity-gated (title contains CELSIUS on every fetched snapshot; note
an earlier attempted ASIN B00TTD9BRC was caught by the identity gate as a
CeraVe product and discarded — the gate is now part of the recipe). Gap:
2022-09 -> 2024-08 (CDX hole for this ASIN). Merge-suspect event: +32,456
ratings in 60 days (2022-06-14 -> 2022-08-13) coinciding with a title change
("Fitness... Standard Variety" -> "Essential... Official Variety") — flagged in
scoring. Series: 20211124 35,042 4.7 · 20220309 41,850 4.7 · 20220614 49,354
4.7 · 20220813 81,810 4.7 (merge-suspect) · 20240901 97,593 4.6 · 20241201
106,448 4.6 · 20250318 110,765 4.6 · 20250612 112,688 4.6 (row-level `id_`
URLs in `scratchpad` build log; re-derivable from the recipe).

**S1 CROX** — not reconstructable (see Part-1 apparel row); all CROX S1 reads
scored too_thin with the pool re-parent event as evidence.

**S2 all tickers** — Wikimedia pageviews REST API, monthly, 2021-01 -> 2026-06.
ELF stitched across the 2024-09 rename (old title `E.l.f._(cosmetics)` through
2024-08, `E.l.f.` from 2024-09; stitch derived from the redirect's edit
history). CELH article young: data only from 2024-02 -> all four CELH S2 reads
too_thin (article-age truncation, reported, not hidden). EL/ULTA/CROX full
coverage.

**Outcomes** — EDGAR companyfacts for all 5 tickers (CIKs 1600033, 1001250,
1403568, 1341766, 1334036), quarterly revenue with YoY, filing dates, 8-K
dates; continuity and arithmetic spot-verified; Q4-derivation and tag caveats
recorded. Entity flags: CROX 2022-2023 outcomes include HeyDude (acquired
2022-02); CELH 2025-06 outcome includes Alani Nu (inorganic jump).

### Scored correspondence table (verbatim scoring output)

| ticker | cutoff | series | signal_read | signal_notes | outcome_read | outcome (YoY now vs prev) | outcome_flag | correspondence |
|---|---|---|---|---|---|---|---|---|
| ELF | 2022-12-31 | S1 wayback_ratings | too_thin | only 1 usable point(s) <= cutoff | accelerating | +49.3% vs +33.2% |  | too_thin |
| ELF | 2022-12-31 | S2 wiki_pageviews | too_thin | coverage gap (article age or rename) | accelerating | +49.3% vs +33.2% |  | too_thin |
| ELF | 2023-03-31 | S1 wayback_ratings | too_thin | only 2 usable point(s) <= cutoff | accelerating | +78.2% vs +49.3% |  | too_thin |
| ELF | 2023-03-31 | S2 wiki_pageviews | accelerating | YoY +31% vs prior +8% (q=17605) | accelerating | +78.2% vs +49.3% |  | MATCH |
| ELF | 2024-12-31 | S1 wayback_ratings | accelerating | v_now=31.5/d v_prev=-11.9/d (+364%); coverage-degraded: last point 145d before cutoff; flag@20240602: purge -1108 in window | decelerating | +31.1% vs +39.7% |  | MISS |
| ELF | 2024-12-31 | S2 wiki_pageviews | accelerating | YoY -9% vs prior -27% (q=25333) | decelerating | +31.1% vs +39.7% |  | MISS |
| ELF | 2025-03-31 | S1 wayback_ratings | accelerating | v_now=29.0/d v_prev=22.7/d (+28%) | decelerating | +3.6% vs +31.1% |  | MISS |
| ELF | 2025-03-31 | S2 wiki_pageviews | decelerating | YoY -31% vs prior -9% (q=26278) | decelerating | +3.6% vs +31.1% |  | MATCH |
| CELH | 2022-06-30 | S1 wayback_ratings | accelerating | v_now=77.4/d v_prev=64.8/d (+19%) | decelerating | +136.7% vs +166.6% |  | MISS |
| CELH | 2022-06-30 | S2 wiki_pageviews | too_thin | coverage gap (article age or rename) | decelerating | +136.7% vs +166.6% |  | too_thin |
| CELH | 2022-09-30 | S1 wayback_ratings | accelerating | v_now=540.9/d v_prev=77.4/d (+599%); coverage-degraded: last point 48d before cutoff; flag@20220813: merge-suspect (+32k/60d, title change) | decelerating | +98.3% vs +136.7% |  | MISS |
| CELH | 2022-09-30 | S2 wiki_pageviews | too_thin | coverage gap (article age or rename) | decelerating | +98.3% vs +136.7% |  | too_thin |
| CELH | 2025-03-31 | S1 wayback_ratings | decelerating | v_now=40.3/d v_prev=97.3/d (-59%) | decelerating | -7.4% vs -4.4% |  | MATCH |
| CELH | 2025-03-31 | S2 wiki_pageviews | too_thin | coverage gap (article age or rename) | decelerating | -7.4% vs -4.4% |  | too_thin |
| CELH | 2025-06-30 | S1 wayback_ratings | decelerating | v_now=22.4/d v_prev=40.3/d (-45%) | accelerating | +83.9% vs -7.4% | inorganic-outcome (Alani Nu acquisition) | MISS |
| CELH | 2025-06-30 | S2 wiki_pageviews | too_thin | coverage gap (article age or rename) | accelerating | +83.9% vs -7.4% | inorganic-outcome (Alani Nu acquisition) | too_thin |
| CROX | 2022-12-31 | S1 wayback_ratings | too_thin | series not reconstructable (variant pool re-parent: 38->336,875 in 19d) | accelerating | +61.1% vs +57.4% | outcome includes HeyDude (acq. Feb 2022) | too_thin |
| CROX | 2022-12-31 | S2 wiki_pageviews | accelerating | YoY +32% vs prior +9% (q=116131) | accelerating | +61.1% vs +57.4% | outcome includes HeyDude (acq. Feb 2022) | MATCH |
| CROX | 2023-03-31 | S1 wayback_ratings | too_thin | series not reconstructable (variant pool re-parent: 38->336,875 in 19d) | decelerating | +33.9% vs +61.1% | outcome includes HeyDude lap effects | too_thin |
| CROX | 2023-03-31 | S2 wiki_pageviews | accelerating | YoY +37% vs prior +32% (q=113583) | decelerating | +33.9% vs +61.1% | outcome includes HeyDude lap effects | MISS |
| CROX | 2025-12-31 | S1 wayback_ratings | too_thin | series not reconstructable (variant pool re-parent: 38->336,875 in 19d) | accelerating | -3.2% vs -6.2% |  | too_thin |
| CROX | 2025-12-31 | S2 wiki_pageviews | accelerating | YoY -9% vs prior -19% (q=95248) | accelerating | -3.2% vs -6.2% |  | MATCH |
| CROX | 2026-03-31 | S1 wayback_ratings | too_thin | series not reconstructable (variant pool re-parent: 38->336,875 in 19d) | steady | -1.7% vs -3.2% |  | too_thin |
| CROX | 2026-03-31 | S2 wiki_pageviews | decelerating | YoY -16% vs prior -9% (q=75564) | steady | -1.7% vs -3.2% |  | adjacent |
| EL | 2025-12-31 | S2 wiki_pageviews | steady | YoY -10% vs prior -10% (q=67969) | steady | +5.6% vs +3.6% |  | MATCH |
| EL | 2026-03-31 | S2 wiki_pageviews | accelerating | YoY +48% vs prior -10% (q=101507) | steady | +4.6% vs +5.6% |  | adjacent |
| ULTA | 2026-01-31 | S2 wiki_pageviews | accelerating | YoY +46% vs prior +23% (q=50482) | steady | +11.8% vs +12.9% |  | adjacent |
| ULTA | 2026-05-02 | S2 wiki_pageviews | decelerating | YoY +20% vs prior +46% (q=45796) | steady | +11.1% vs +11.8% |  | adjacent |

**Totals: 28 reads -> scoreable 17 (MATCH 6, adjacent 4, MISS 7); too_thin 11.**

### Honest reading of the Part-2 result

- **Directional correspondence on this tiny in-sample set is mixed —
  approximately coin-flip (6 MATCH vs 7 MISS among 17 scoreable reads).** This
  neither validates nor kills the momentum hypothesis; at n=17 with
  outcome-aware quarter selection, it says: reconstruction is feasible enough
  to run the test, and the test does not produce an obvious strong signal on
  its own.
- **The instrument, not the signal, drove 11/28 reads to too_thin** — archive
  gaps (ELF 2022, CELH 2023), article-age truncation (CELH pageviews), and the
  Crocs pool-identity failure. A live-captured (Class-A) series would have had
  none of these holes. That asymmetry is the probe's clearest product lesson.
- **The most instructive single row:** CELH 2025-06 — the reconstructed Amazon
  SKU velocity correctly tracked decelerating ORGANIC brand demand while
  consolidated revenue jumped +84% on the Alani Nu acquisition. Scored MISS by
  rule, but the "miss" is an entity-mapping artifact: brand-level signal vs
  ticker-level consolidated outcome. Any real backtest must resolve
  brand->entity->ticker before scoring (the thesis already names
  entity-resolution as load-bearing; this is empirical confirmation).
- **Divergent same-ticker reads are informative:** at ELF 2025-03, Amazon
  ratings velocity said accelerating while pageviews said decelerating and the
  outcome decelerated — single-SKU Amazon proxies capture channel-local demand,
  not total demand. Multi-venue confirmation is not optional.
- Both series missed ELF 2024-12 (both improving while growth decelerated) —
  with n this small that may be noise, channel mix, or lead/lag misalignment;
  recorded, not explained away.

## Feasibility verdict (the owner's decision surface)

1. **Is zero-lookahead reconstruction feasible?** Yes, narrowly: for mono-SKU
   staple products via Wayback counters, for attention via Wikipedia pageviews
   (with stitch/age caveats), and for filed outcomes via EDGAR — all free and
   re-runnable. No, or gated: dated reviews at the source (closed), Reddit
   mentions (ToS adjudication owned by the capture lane), YouTube at scale
   (keyed API), TikTok/IG (structurally closed), multi-variant apparel PDPs
   (pool identity unstable).
2. **Does reconstructed signal correspond to filed outcomes well enough to
   justify designing a real backtest?** The honest answer from n=17:
   *undetermined but testable* — the pipes work end-to-end, the costs are
   small, and the observed failure modes are all addressable by design choices
   (multi-venue confirmation, entity resolution, organic/inorganic outcome
   splitting, denser series). A real test needs: pre-registered quarters chosen
   blind to outcomes, brand->ticker entity mapping done first, 5-10x more
   (ticker, quarter) cells, and at least two independent venues per subject.
3. **What the probe adds to the moat doctrine (PR #832):** live, dated
   observations of Class-B decay (venue closure, counter de-rendering, purge,
   pool merges, rename fragmentation, article-age truncation) — strengthening
   the doctrine's core claim that only Class-A live capture compounds reliably.
   No revision to the taxonomy is proposed.

## Boundaries honored and accepted residuals

- Probe tier held: no standing pipelines, monitors, dashboards, models, capture
  scale-up, outreach, or publishing. Stop condition reached: both parts
  reported.
- Evidence is screening-tier (URLs + dates + extracted counters), not
  packet-grade armory capture; if any series is later promoted to evidence for
  a real backtest, it re-runs through the Runner Ladder as a capture-lane act.
- Residuals accepted for this tier: single-SKU Amazon proxies; n=17 scoreable
  cells; outcome-aware quarter selection (disclosed); S1 row-level `id_` URLs
  for ELF live in the lane transcript/scratch rather than this report (fully
  re-derivable from the recipes below); ULTA fiscal quarters approximated to
  month boundaries for S2 binning.

## Follow-ups (named, not performed)

1. **Packet `stale_if` update** — the commissioning packet lives on PR #832 and
   is not on `main`; when #832 merges, add a pointer from the packet's
   `stale_if` to this report (one-line follow-up edit on a fresh lane or by the
   owner).
2. **Capture-lane adjudications** (owner/capture-lane): Pushshift-lineage
   reliance posture; YouTube Data API keyed route; Ulta listing-page extraction
   as a capture family.
3. **If the owner wants the real test**: commission a pre-registered forward
   design (blind quarter selection, entity mapping first, multi-venue), which
   is a separate decision this report deliberately does not start.

## Re-run recipes (all scoring reproducible from these)

- Wayback CDX (per ASIN, both URL forms; keep rows with length>100000):
  `https://web.archive.org/cdx/search/cdx?url=amazon.com/dp/<ASIN>&output=json&from=20211001&to=20251231&filter=statuscode:200&collapse=timestamp:6&limit=80`
  plus the slug-form URL variant, plus `&matchType=prefix` where density is thin.
  Snapshot fetch: `https://web.archive.org/web/<TS>id_/<original-url>`; extract
  first `acrCustomerReviewText[^>]*>([\d,]+) ratings` (fallback
  `"ratingCount"[^0-9]*([\d,]+)`), `([\d.]+) out of 5 stars`, `<title>` identity
  gate (title must match the intended product/brand).
- Wikipedia pageviews:
  `https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/<TITLE>/monthly/<FROM>/<TO>`;
  resolve canonical titles AND rename history first
  (`action=query&prop=revisions&titles=<redirect>` on the redirects); stitch
  old-title months before the move, new-title months after.
- EDGAR: CIKs via `https://www.sec.gov/files/company_tickers.json`; facts via
  `https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json` (tags:
  RevenueFromContractWithCustomerExcludingAssessedTax, fallback Revenues; Q4 =
  FY minus Q1-Q3 where no discrete Q4 is filed); 8-K dates via
  `https://data.sec.gov/submissions/CIK##########.json` (Item 2.02 match).
- Scoring: cutoffs = fiscal period_end; S1 velocity from the last three <=cutoff
  points (accel/decel at +/-10% velocity delta); S2 quarterly YoY delta at 2pp;
  outcome YoY delta at 2pp; correspondence MATCH/adjacent/MISS/too_thin
  (too_thin if <3 points or coverage gap). Quarter-selection rule and the one
  disclosed amendment are stated in the Part-2 pre-registration section.

## Non-claims

Not validation, not readiness, not buyer proof, not willingness-to-pay, not a
track record, not a hit-rate estimate, not capture authorization, not a
route/ToS decision, not a product-shape decision, not doctrine ratification,
and not a change to the moat doctrine, thesis, or any capture-lane record. The
"momentum is not priced in" idea remains an untested hypothesis; this probe
only established what a test would cost and which instruments survive contact
with July-2026 reality.
