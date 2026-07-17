# Tower 28 Beauty — Phase 1 CSB-First Company-Intelligence Scan v1

```text
retrieval_header_version: 1
artifact_role: Research artifact (CSB-first bounded scan receipt — Tower 28 Phase 1)
scope: Sealed scan receipt for the Tower 28 Phase 1 company-intelligence commission.
  Records the broad-scout phase, exact-query discovery, venue evaluations, hidden-venue
  pointers, screen-light observations, negatives, access notes, and capture requests
  produced under docs/research/forseti_beauty_tower28_company_intelligence_csb_v1.md.
use_when:
  - Writing or auditing the Phase 1 CI report (docs/research/forseti_beauty_tower28_company_intelligence_report_v1.md).
  - Tracing any Phase 1 report observation back to its scan move, query, date, and limitation.
authority_boundary: retrieval_only
stale_if:
  - The CSB commission is reissued or the two-phase Tower 28 sequence changes.
  - A later scan supersedes this receipt.
note: header uses a text fence intentionally so the intake receipt below is the first
  yaml block the scan checker parses.
```

## Scan Intake Receipt

```yaml
commission_id: tower28_ci_phase1_2026_07_16
scan_receipt_version: 1
scan_date: "2026-07-16"
scan_completed: "2026-07-17 (Asia/Singapore vantage; moves dated individually)"
mode: forward
subject: Tower 28 Beauty (resolved Brand; owning entity Tower 28 Beauty, Inc., Los Angeles)
source_context_status: SOURCE_CONTEXT_READY
run_caps:
  max_screening_moves_total: 40
  max_exact_queries_total: 30
  cap_convention: >
    UNIT DEFINITION (do not mix units when reading this receipt): the capped
    and counted unit is the ORCHESTRATOR-LEDGER MOVE — one bounded orchestrator
    read/attempt, or one bounded delegated sub-scout run counted as a single
    move. By that unit, 24 of 40 were used. The five sub-scout runs comprise 101
    internal web operations in aggregate (search + fetch calls per the move
    ledger: 23 + 22 + 15 + 21 + 20), so total web operations across the scan
    were approximately 120; that aggregate is
    disclosed for transparency but is NOT the capped unit — each sub-scout was
    separately bounded by the per-scout budget stated in its dispatch and
    reported in its return. The intake field names (screening_moves_used,
    max_screening_moves_total) are fixed by the scan checker contract and
    therefore keep the ledger-move unit. Exact queries carry EQ ids only when
    load-bearing for CSB-row accountability; additional sub-scout query strings
    are accounted inside the per-scout aggregate totals.
screening_moves_used: 24
exact_queries_used: 20
hidden_venue_pointers: 10
capture_requests: 3
closeout_state: capture_preservation_only
```

## Broad Scout Accounting

The default bounded broad-scout phase ran as one route-ledger sub-scout (M20:
15 searches + 8 fetches) on 2026-07-16, miss-checking the CSB board before main
deepening. Its return was route-shaped: frontiers checked across retail, trade,
community, registry, and deal-tracker surfaces; exact queries (folded into the
ledger below, EQ-012, EQ-015, EQ-018, EQ-020 among them); venue evals for
planned and unplanned surfaces; hidden venue pointers the board missed (Credo
Beauty, Sephora at Kohl's, Mecca, Pvolve, National Eczema Association seal
ecosystem, INCIDecoder, dupe aggregators); decisive negatives (no Ulta carriage
surfaced in the bounded checks; coupon/deal trackers had no intelligence value);
access notes (WWD Tollbit
paywall, uspto.report 403, community.sephora.com 403 to fetchers); and
recency/current-state notes (2026-04-30 Sephora footprint doubling, 2026-02
Pvolve partnership) with a ranked recommended main-deepening list. Main
deepening (M01, M04, M05, M06, M07, M14, M15 and the remaining sub-scouts)
followed that recommendation. The broad scout minted no candidates, cleared no
gates, and bound no Capture routes.

## CSB Row Accountability

Rows consumed as route map: the commission's coverage ledger rows COV-001
through COV-020 were consumed as this scan's route map under scan-local aliases
SBR-001 through SBR-020 (SBR-NNN = COV-NNN; the commission is a company-profile
board, so its rows are COV-prefixed).

| CSB row (alias) | Route | Scan outcome |
| --- | --- | --- |
| SBR-001 (brand site home) | pre-checked seed | re-deepened via M22 (positioning, promo state) |
| SBR-002 (Sephora search) | pre-checked seed | deepened via M01 (full 25-item assortment state) |
| SBR-003 (Revolve search) | pre-checked seed | direct re-read blocked (M19); carriage corroborated by brand stores page (M22) |
| SBR-004 (Reddit bounded scout) | executed | M02, M03, M04, M05, M06, M07 listings; M12, M13 thread attempts login-refused; graph seam still DEPENDENCY_PENDING |
| SBR-005 (Quora experimental scout) | executed | M16 login wall + EQ-011 zero index → blocked_with_typed_gap |
| SBR-006 (category-aware specialist forums) | executed | discovered: Sephora BIC (now read-only archive), Thingtesting, dupe aggregators, eczema blogs; MakeupAlley zero yield (EQ-019) |
| SBR-007 (Sephora reviews/Q&A) | partially executed | review-count and rating state captured at brand-page level (M01); per-review text sampling deferred to report-stage need; BIC threads verified (M14, M15) |
| SBR-008 (Ulta carriage check) | executed | no carriage surfaced via EQ-015 + brand stores page M22; direct site read bot-blocked (M17), so this is a bounded negative rather than proof of non-carriage |
| SBR-009 (Amazon presence) | partially executed | geo-vantage redirect to amazon.sg (M18): International Store carries Tower 28; US seller state → capture request CR-003 |
| SBR-010 (Sephora PDP state) | partially executed | assortment/price/rating state via M01; per-PDP promotion/badge detail not separately read |
| SBR-011 (brand PDP claims/prices) | executed | M22 catalog, prices, claims, sold-out flags |
| SBR-012 (TikTok public) | not executable in-lane | not separately authorized; titles known from search indexing only → CR-002 |
| SBR-013 (Instagram public) | not executable in-lane | same boundary as SBR-012 |
| SBR-014 (YouTube public) | executed | M24 screen-light shortlist; upload dates snippet-level |
| SBR-015 (search-surface exact-query walk) | executed | EQ-010 through EQ-020 families via M20, M23, M24 |
| SBR-016 (AEO answer engines) | not run | conditional row; deferred — ordinary-SERP venue dominance noted instead (M24); typed gap in closeout |
| SBR-017 (trade press) | executed | M21 dated chronology 2022-2026 |
| SBR-018 (careers/ATS + leadership) | executed | M22 careers page; M21 leadership negatives |
| SBR-019 (brand press/announcements) | executed | M22 blog dates; no dedicated press page (negative) |
| SBR-020 (registries/filings) | executed | M21 USPTO marks + owning entity |

## Move Ledger

Orchestrator moves (browser pane and sanctioned harness screening-read entry
`forseti-harness/source_capture/screening_reddit_read.py` per
`docs/decisions/screening_reddit_read_route_decision_v0.md`):

| Move | Date | Surface | What happened |
| --- | --- | --- | --- |
| M01 | 2026-07-16 | sephora.com/brand/tower-28 (browser) | Full 25-item assortment state read (names, prices, ratings, review counts) from page state |
| M02 | 2026-07-16 | old.reddit r/MakeupAddiction search (EQ-001) | 200, 25 dated thread candidates |
| M03 | 2026-07-16 | old.reddit r/SkincareAddiction search (EQ-002) | 200, candidates mostly generic titles (Tower 28 in comments) |
| M04 | 2026-07-17 | old.reddit r/Sephora search (EQ-003) | 200, 25 candidates incl. mascara-rejection and vs-Ciele threads |
| M05 | 2026-07-17 | old.reddit r/beauty search (EQ-004) | 200, 17 candidates incl. brand-evaluation thread 2026-07-02 |
| M06 | 2026-07-17 | old.reddit r/30PlusSkinCare search (EQ-005) | 200, generic titles only — low direct yield |
| M07 | 2026-07-17 | old.reddit r/eczema search (EQ-006) | 200, 13 candidates incl. "tower 28 skincare" 2026-04-24 and hypochlorous-acid threads |
| M12 | 2026-07-17 | old.reddit thread 1unb090 (lipgloss separation) | REFUSED: login page served; screen-light gate stopped read |
| M13 | 2026-07-17 | old.reddit thread 1ty47dw (concealer suck) | REFUSED: login page served |
| M14 | 2026-07-17 | community.sephora.com SOS spray thread (browser) | Verified 2023-06 thread content; forum banner: read-only mode |
| M15 | 2026-07-17 | community.sephora.com concealer thread (browser) | Verified 2024-04-25 complaint + related 2025 threads sidebar |
| M16 | 2026-07-17 | quora.com/search (EQ-007, browser) | Login wall; no anonymous search results |
| M17 | 2026-07-17 | ulta.com search (EQ-008, browser) | Bot interstitial ("Be Right Back"); no result surface |
| M18 | 2026-07-17 | amazon.com search (EQ-009, browser) | Geo-redirect to amazon.sg; International Store carries Tower 28 |
| M19 | 2026-07-17 | revolve.com brand/search (browser) | Search URL navigation denied; generic catalog page only — no brand read |
| M20 | 2026-07-16 | sub-scout: broad scout | 15 searches + 8 fetches; route ledger (see Broad Scout Accounting) |
| M21 | 2026-07-16 | sub-scout: trade press + registries | 11 searches + 11 fetches; dated chronology + USPTO |
| M22 | 2026-07-16 | sub-scout: owned channels | 1 search + 14 fetches; catalog, claims, careers, stores, blog |
| M23 | 2026-07-16 | sub-scout: community snippets | 16 searches + 5 fetches; snippet-level community language + thread shortlist |
| M24 | 2026-07-16 | sub-scout: creator video + search walk | 12 searches + 8 fetches; YouTube shortlist + SERP language walk |

Reddit listing re-reads: M08, M09, M10, M11 (2026-07-17) repeated the
r/Sephora, r/beauty, r/30PlusSkinCare, and r/eczema listing GETs of the pass-1
run because pass-1 output was truncated before those subreddits printed; they
are counted as moves because they were real bounded GETs (2.5s spacing,
human-rate).

## Exact Query Discovery Ledger

| EQ id | Query (verbatim or URL-shaped) | Intent | Result class | Next-route decision |
| --- | --- | --- | --- | --- |
| EQ-001 | old.reddit.com/r/MakeupAddiction/search?q=Tower%2028&restrict_sr=on&sort=new&t=year | test SBR-004 | yield (25 candidates) | deepen failure-mode threads → login wall → CR-001 |
| EQ-002 | same, r/SkincareAddiction | test SBR-004 | mixed (generic titles) | low direct yield; no deepening |
| EQ-003 | same, r/Sephora | test SBR-004 | yield | mascara-rejection + vs-Ciele threads to CR-001 |
| EQ-004 | same, r/beauty | test SBR-004 | yield | brand-evaluation thread 2026-07-02 to CR-001 |
| EQ-005 | same, r/30PlusSkinCare | test SBR-004 | low yield | close branch |
| EQ-006 | same, r/eczema | test SBR-004 need-state | yield | eczema/HOCl threads to CR-001 |
| EQ-007 | quora.com/search?q="Tower 28" beauty | SBR-005 experimental scout | blocked (login wall) | typed gap; no lawful anonymous route found |
| EQ-008 | ulta.com/search?query=Tower 28 | SBR-008 carriage check | blocked (bot interstitial) | rely on EQ-015 + brand stores page |
| EQ-009 | amazon.com/s?k=Tower+28+Beauty | SBR-009 seller state | partial (geo-redirect to .sg) | CR-003 for US-vantage read |
| EQ-010 | site:reddit.com "Tower 28" (web search) | SBR-004 snippet floor | zero (decisive negative: search engine no longer indexes usable reddit links) | escalate to sanctioned old.reddit listing route (EQ-001 family) |
| EQ-011 | site:quora.com "Tower 28" beauty (web search) | SBR-005 snippet floor | zero | corroborates Quora typed gap |
| EQ-012 | "dupe for Tower 28" (web search) | substitution language | yield | dupe aggregators (SkinSort, Brandefy, SkinsKool, Beautymasterlist, Temptalia) |
| EQ-013 | "stopped using Tower 28" / "Tower 28 broke me out" (web search) | failure/switching language | yield | TikTok topic pages (titles only) + Sephora BIC threads → M14, M15 |
| EQ-014 | "Tower 28 vs …" family (web search) | comparison set | yield | comparison pairs: Saie, Kosas, NARS, Hourglass, Ciele, Supergoop, NYX (dupe), Summer Fridays, Rhode, Merit |
| EQ-015 | "Tower 28 Beauty Ulta Kohl's retailer expansion" (web search) | channel facts | yield | no Ulta carriage surfaced; Sephora at Kohl's positive |
| EQ-016 | "Tower 28 Beauty funding investment 2025 2026" (web search) | ownership/funding events | zero (no new round/acquisition found) | negative recorded |
| EQ-017 | "Tower 28 Beauty lawsuit OR National Advertising Division OR recall" (web search) | claims/regulatory events | zero | negative recorded |
| EQ-018 | "is tower 28 clean" (web search) | claims language venues | yield | editorial/blog venues dominate; EWG and INCIDecoder surfaced |
| EQ-019 | MakeupAlley "Tower 28" (web search) | specialist forum check | zero via search index | not deepened; venue possibly alive but not surfaced |
| EQ-020 | "Tower 28 Beauty news 2026" (web search) | recency anchor | yield | BeautyMatter 2026-04-30 + Pvolve 2026-02 → main deepening |

No query count, search rank, module recurrence, or repeated result presence was
treated as demand proof; queries routed attention only.

## Venue Evaluation

| Venue | Worth deepening for this commission | Basis (screen-light) |
| --- | --- | --- |
| r/MakeupAddiction | yes — highest-yield live buyer-language venue | dated Tower-28-titled threads incl. failure modes, pairing questions, hauls |
| r/Sephora | yes | rejection/switching and comparison threads with dates |
| r/beauty | yes | brand-evaluation and shade-range threads |
| r/eczema | yes (need-state) | SOS-line and hypochlorous-acid threads; brand's core sensitive-skin population |
| r/SkincareAddiction, r/30PlusSkinCare | low direct value | Tower 28 appears in comments, not titles; deepening requires thread bodies (login-walled) |
| Sephora Beauty Insider Community | archival only — forum now read-only | verified banner (M14); rich 2023-2025 threads remain readable as history |
| Quora | no current route | login-walled search + zero search-index presence |
| MakeupAlley | unknown/low | zero search-index yield this pass |
| TikTok | high relevance, not authorized in-lane | complaint-theme and comparison topic pages visible in search indexing only |
| YouTube | moderate | comparison genre is dense; metadata (dates/sponsorship) not verifiable screen-light |
| Dupe aggregators (SkinSort, Brandefy, SkinsKool, Beautymasterlist, Temptalia) | yes (substitution/price language) | SEO/affiliate caveat; several 403 to fetchers |
| Thingtesting | potential (repurchase-style community voting) | 403 to fetchers; unverified |
| Trade press (BeautyMatter, Drug Store News; WWD paywalled) | yes | dated chronology; syndication risk flagged |
| INCIDecoder / EWG | yes (claims verification support) | accessible; product-level ingredient framing |
| Brand owned channels | yes | catalog/claims/careers/stores state readable; intermittent 503 then OK |
| Credo Beauty, Sephora at Kohl's, Mecca, TikTok Shop, Pvolve | yes (channel surfaces the board under-specified) | brand stores page + trade press |
| Coupon/deal trackers | no | generic promo content, no intelligence value |

## Hidden Venue Pointers

```yaml
hidden_venue_pointers:
  - hidden_venue_pointer_id: HVP-001
    venue: Credo Beauty (credobeauty.com/collections/tower-28)
    why: clean-beauty retailer carriage absent from the board's channel rows; brand stores page lists six Credo cities
  - hidden_venue_pointer_id: HVP-002
    venue: Sephora at Kohl's (kohls.com Tower 28 catalog)
    why: distribution channel named in brand-attributed GMV figure; board had no Kohl's row
  - hidden_venue_pointer_id: HVP-003
    venue: Mecca (AU/NZ, mecca.com.au)
    why: international channel listed by brand stores page; corroborates non-US expansion
  - hidden_venue_pointer_id: HVP-004
    venue: TikTok Shop (brand-listed sales channel)
    why: listed as a selling channel by the brand itself; distinct from TikTok content surfaces
  - hidden_venue_pointer_id: HVP-005
    venue: Pvolve fitness-studio partnership (drugstorenews.com 2026-02)
    why: experiential/wellness channel motion not on the board
  - hidden_venue_pointer_id: HVP-006
    venue: National Eczema Association ecosystem (nationaleczema.org press releases)
    why: seal/partnership surface for the sensitive-skin need-state; primary-source credibility facts
  - hidden_venue_pointer_id: HVP-007
    venue: INCIDecoder brand hub (incidecoder.com/brands/tower-28)
    why: ingredient-level claims verification support surface
  - hidden_venue_pointer_id: HVP-008
    venue: Dupe aggregators (skinsort.com, brandefyskin.com, skinskoolbeauty.com, beautymasterlist.com, temptalia.com)
    why: named substitution/price-comparison set for hero SKUs
  - hidden_venue_pointer_id: HVP-009
    venue: Thingtesting brand page (thingtesting.com/brands/tower-28)
    why: community repurchase-style voting on SOS spray; fetch-blocked, unverified
  - hidden_venue_pointer_id: HVP-010
    venue: Independent eczema-reviewer blogs (e.g., whimsysoul.com 2026-04-16 review)
    why: dated first-person need-state experience outside platform venues
```

## Screen-Light Observations

Note on vocabulary: this is a decision-neutral company-intelligence scan;
`candidate_support` below means "supports a Phase 1 company-report fact," not a
demand candidate. Public-reaction counts (review counts, ratings) appear as
routing/dispersion context only — they are not demand proof, sell-through,
credibility, or gate evidence.

```yaml
observations:
  - observation_id: SOBS-001
    source_move_id: M01
    url: https://www.sephora.com/brand/tower-28
    retrieval_date: "2026-07-16"
    short_quote_or_summary: "25 Tower 28 items live at Sephora US incl. a seven-product SOS skincare family listed under eight catalog tokens (spray + its jumbo refill counted as one product, moisturizer, cleanser, serum, lip balm, body wash, SPF)."
    signal_stage: candidate_support
    claim_it_might_support: current Sephora assortment breadth and observable makeup-to-skincare line expansion
    gate_role: none
    independence_hypothesis: retailer catalog state; independent of brand announcements in form, though assortment itself is a joint brand-retailer decision
    uncertainty_or_limits: page-state observation; assortment is not velocity, sell-through, or productivity
  - observation_id: SOBS-002
    source_move_id: M01
    url: https://www.sephora.com/brand/tower-28
    retrieval_date: "2026-07-16"
    short_quote_or_summary: "Rating dispersion: ShineOn 4.46 (5.6K), BeachPlease 4.47 (1.9K), GetSet blush 4.57, Swipe 4.34 (3.7K) vs MakeWaves 3.82 (3.0K), GetSet powder 3.71, SuperDew 3.56, SunnyDays tint 3.98 (1.9K), SOS spray 4.09 (4.9K)."
    signal_stage: candidate_support
    claim_it_might_support: product-reception dispersion across the line — hero items rate materially higher than several complexion/eye items
    gate_role: none
    independence_hypothesis: aggregated customer reviews at one retailer; not independent across products (same platform conventions)
    uncertainty_or_limits: ratings and counts are reception proxies with ceilings — not sell-through, repeat purchase, or representative demand
  - observation_id: SOBS-003
    source_move_id: M01
    url: https://www.sephora.com/brand/tower-28
    retrieval_date: "2026-07-16"
    short_quote_or_summary: "SOS spray priced $12 (mini) to $68 (jumbo refill); Swipe $24; ShineOn $16; SunnyDays tint $32; FaceGuard SPF $18-$32."
    signal_stage: candidate_support
    claim_it_might_support: current price architecture at Sephora
    gate_role: none
    independence_hypothesis: retailer page state
    uncertainty_or_limits: point-in-time; promotions not captured at PDP level
  - observation_id: SOBS-004
    source_move_id: M02
    url: https://old.reddit.com/r/MakeupAddiction/comments/1unb090/tower_28_lipgloss_causing_makeup_separation/
    retrieval_date: "2026-07-16"
    short_quote_or_summary: "Thread titled 'Tower 28 lipgloss causing makeup separation?' posted 2026-07-04."
    signal_stage: candidate_support
    claim_it_might_support: dated, product-specific failure-mode question in a live buyer venue (title-level evidence)
    gate_role: none
    independence_hypothesis: organic user post (hypothesis); body unread — login-walled to the sanctioned screening route
    uncertainty_or_limits: title only; content, resolution, and responses unknown → CR-001
  - observation_id: SOBS-005
    source_move_id: M02
    url: https://old.reddit.com/r/MakeupAddiction/comments/1ty47dw/anyone_elses_tower_28_concealer_suck/
    retrieval_date: "2026-07-16"
    short_quote_or_summary: "Thread titled 'anyone elses tower 28 concealer suck?' posted 2026-06-06."
    signal_stage: candidate_support
    claim_it_might_support: dated rejection-language datum on the hero concealer (title-level)
    gate_role: none
    independence_hypothesis: organic user post (hypothesis); body unread
    uncertainty_or_limits: title only; a provocative title is not a measured complaint rate → CR-001
  - observation_id: SOBS-006
    source_move_id: M02
    url: https://old.reddit.com/r/MakeupAddiction/comments/1u8tv04/my_first_tower_28_haul_all_ready_for_the_summer/
    retrieval_date: "2026-07-16"
    short_quote_or_summary: "Advocacy/choice threads: 'My first tower 28 haul' (2026-06-18); 'What powder goes well with the Tower 28 concealer?' (2026-06-23)."
    signal_stage: candidate_support
    claim_it_might_support: live acquisition and use-context conversation in the same venue as the failure-mode threads
    gate_role: none
    independence_hypothesis: organic user posts (hypothesis)
    uncertainty_or_limits: titles only; no body text
  - observation_id: SOBS-007
    source_move_id: M08
    url: https://old.reddit.com/r/Sephora/comments/1tsw0kd/
    retrieval_date: "2026-07-17"
    short_quote_or_summary: "Thread titled 'Don't like Tower 28 mascara - where to go from here?' posted 2026-05-31."
    signal_stage: candidate_support
    claim_it_might_support: dated mascara rejection with explicit switching intent (title-level); coheres with MakeWaves 3.82 rating state (SOBS-002)
    gate_role: none
    independence_hypothesis: organic user post (hypothesis)
    uncertainty_or_limits: title only; single instance, not a rate
  - observation_id: SOBS-008
    source_move_id: M08
    url: https://old.reddit.com/r/Sephora/comments/1te380p/
    retrieval_date: "2026-07-17"
    short_quote_or_summary: "Thread titled 'Tower 28 vs Ciele skin tint review' posted 2026-05-15."
    signal_stage: candidate_support
    claim_it_might_support: live comparison-set datum (skin tint vs Ciele)
    gate_role: none
    independence_hypothesis: organic user review (hypothesis)
    uncertainty_or_limits: title only
  - observation_id: SOBS-009
    source_move_id: M09
    url: https://old.reddit.com/r/beauty/comments/1ulo4kf/
    retrieval_date: "2026-07-17"
    short_quote_or_summary: "Thread titled 'What are people's thoughts on Tower 28?' posted 2026-07-02."
    signal_stage: candidate_support
    claim_it_might_support: current open brand-evaluation conversation among buyers
    gate_role: none
    independence_hypothesis: organic user post (hypothesis)
    uncertainty_or_limits: title only; responses unread → CR-001
  - observation_id: SOBS-010
    source_move_id: M09
    url: https://old.reddit.com/r/beauty/comments/1q4k9hv/
    retrieval_date: "2026-07-17"
    short_quote_or_summary: "2026-01-05 thread seeking pale-olive concealer explicitly excluding 'Tower 28 BU' as too dark/limited."
    signal_stage: candidate_support
    claim_it_might_support: shade-range boundary language for Swipe (title-level)
    gate_role: none
    independence_hypothesis: organic user post (hypothesis)
    uncertainty_or_limits: "over-180-day tier — chronology/recurrence context only, never current-pressure evidence"
  - observation_id: SOBS-011
    source_move_id: M11
    url: https://old.reddit.com/r/eczema/comments/1sum1co/tower_28_skincare/
    retrieval_date: "2026-07-17"
    short_quote_or_summary: "r/eczema threads: 'tower 28 skincare' (2026-04-24); 'Make up for Eczema prone skin?' (2026-05-15); hypochlorous-acid comparison threads (2025-12)."
    signal_stage: venue_value
    claim_it_might_support: the eczema need-state community actively discusses the SOS line and its ingredient class
    gate_role: none
    independence_hypothesis: organic need-state community (hypothesis)
    uncertainty_or_limits: titles only; bodies login-walled → CR-001
  - observation_id: SOBS-012
    source_move_id: M12
    url: https://old.reddit.com/r/MakeupAddiction/comments/1unb090/tower_28_lipgloss_causing_makeup_separation/
    retrieval_date: "2026-07-17"
    short_quote_or_summary: "Thread-body reads refused: Reddit served login/register pages to the sanctioned screening route for comment pages."
    signal_stage: access_note
    claim_it_might_support: Reddit thread bodies are outside the current screen-light route; listings remain readable
    gate_role: none
    independence_hypothesis: not_applicable
    uncertainty_or_limits: applies to M12 and M13; basis for CR-001
  - observation_id: SOBS-013
    source_move_id: M14
    url: https://community.sephora.com/t5/Skincare-Aware/tower-28-SOS-spray/m-p/6587314
    retrieval_date: "2026-07-17"
    short_quote_or_summary: "Banner: 'The Beauty Insider Community Forum is now in read-only mode.'"
    signal_stage: venue_value
    claim_it_might_support: Sephora BIC is an archival venue — historical language remains readable, but no new customer conversation accrues there
    gate_role: none
    independence_hypothesis: platform-operator statement
    uncertainty_or_limits: read-only start date not established
  - observation_id: SOBS-014
    source_move_id: M14
    url: https://community.sephora.com/t5/Skincare-Aware/tower-28-SOS-spray/m-p/6587314
    retrieval_date: "2026-07-17"
    short_quote_or_summary: "2023-06 verified quotes: eczema flare relief ('I'm going through yet another flare up of eczema and it calms right down') and cheaper-substitute advice ('other hypochlorous acid sprays... cost quite a bit less', naming SkinSmart)."
    signal_stage: candidate_support
    claim_it_might_support: recurrence context — eczema-relief use case and price-substitution logic around SOS existed by mid-2023
    gate_role: none
    independence_hypothesis: peer forum users; platform has commercial interest in brands it sells
    uncertainty_or_limits: "over-180-day tier; chronology/recurrence only"
  - observation_id: SOBS-015
    source_move_id: M15
    url: https://community.sephora.com/t5/Customer-Support/Tower-28-concealer/m-p/6907386
    retrieval_date: "2026-07-17"
    short_quote_or_summary: "2024-04-25 verified complaint: Swipe 'marketed as an acne safe brand... but it has pore clogging ingredients', naming Polyglyceryl-3 Diisostearate against Sephora PDP copy 'non-comedogenic'. Sidebar shows related threads through 2025-07 ('Tower 28 concealer creasing')."
    signal_stage: contradiction
    claim_it_might_support: a documented claims-versus-experience contradiction on the hero concealer, with recurrence pointers into 2025
    gate_role: none
    independence_hypothesis: single customer complaint; ingredient comedogenicity assertion is the customer's, not a test result
    uncertainty_or_limits: "over-180-day tier for the anchor post; related 2025 threads unread; one complaint is not a rate"
  - observation_id: SOBS-016
    source_move_id: M21
    url: https://beautymatter.com/articles/tower-28-expands-its-sephora-footprint
    retrieval_date: "2026-07-16"
    short_quote_or_summary: "BeautyMatter 2026-04-30: Sephora NA footprint doubled 4→8 shelves across ~500 doors; brand-attributed $119M GMV across Amazon, Sephora, Sephora at Kohl's 'in the past year'; Swipe cited as a top-3 Sephora NA concealer; Sephora Middle East launch across 55 doors; quote: 'we were literally bursting out of our space' (Amy Liu)."
    signal_stage: candidate_support
    claim_it_might_support: dated 2026 retail-expansion event and brand-attributed scale markers
    gate_role: decision_event
    independence_hypothesis: independent outlet, but figures are brand-supplied (interview) — one origin, not independent corroboration
    uncertainty_or_limits: GMV/top-3/most-redeemed claims unaudited; trailing period undefined; expansion effective dates not separately stated
  - observation_id: SOBS-017
    source_move_id: M21
    url: https://www.trademarkelite.com/trademark/trademark-detail/97499966/TOWER-28
    retrieval_date: "2026-07-16"
    short_quote_or_summary: "USPTO Reg. 6925089 (filed 2022-07-12, registered 2022-12-13), owner Tower 28 Beauty, Inc., Los Angeles CA; second registration (2024) and additional applications incl. WATERBREAK, SCULPTINO snippet-level."
    signal_stage: candidate_support
    claim_it_might_support: owning legal entity resolution (no parent surfaced anywhere) and possible unreleased product-name pipeline
    gate_role: none
    independence_hypothesis: official registry data via aggregator
    uncertainty_or_limits: second registration and extra marks are snippet-level (uspto.report 403) — unverified by direct read
  - observation_id: SOBS-018
    source_move_id: M21
    url: https://beautymatter.com/articles/tower-28-expands-its-sephora-footprint
    retrieval_date: "2026-07-16"
    short_quote_or_summary: "Negative bundle: no 2025-2026 funding round, acquisition, leadership change, NAD challenge, FDA action, recall, or lawsuit surfaced across targeted queries (EQ-016, EQ-017)."
    signal_stage: negative
    claim_it_might_support: absence of visible ownership/regulatory/legal events in the current window (absence of evidence, bounded by search coverage)
    gate_role: none
    independence_hypothesis: multiple query angles, same search index
    uncertainty_or_limits: paywalled trade press could hold unseen events; absence is not proof
  - observation_id: SOBS-019
    source_move_id: M22
    url: https://www.tower28beauty.com/pages/stores
    retrieval_date: "2026-07-16"
    short_quote_or_summary: "Brand-listed channels: DTC, Sephora (US, Canada, UK, Middle East), Sephora at Kohl's, Credo Beauty (6 cities), Mecca (AU), TikTok Shop, Revolve — Ulta absent; Amazon absent."
    signal_stage: contradiction
    claim_it_might_support: first-party channel set; the Amazon omission sits against the brand-attributed Amazon GMV in SOBS-016 (either an unlisted official channel or third-party/unofficial flow)
    gate_role: none
    independence_hypothesis: official first-party page
    uncertainty_or_limits: page may lag reality; contradiction unresolved → CR-003
  - observation_id: SOBS-020
    source_move_id: M22
    url: https://www.tower28beauty.com/pages/ingredients
    retrieval_date: "2026-07-16"
    short_quote_or_summary: "Brand claims state: 'safe for even the most sensitive skin' (home); 'first and only brand' with NEA + National Rosacea Society + National Psoriasis Foundation seals on all skincare; ingredients page lists exclusions and 3rd-party sensitive-skin/irritation testing; notably does not use 'non-comedogenic' or 'vegan' wording on that page."
    signal_stage: candidate_support
    claim_it_might_support: current claim architecture and a claims-surface divergence — retailer PDP copy (SOBS-015) says 'non-comedogenic' while the brand ingredients page avoids it
    gate_role: none
    independence_hypothesis: official first-party pages
    uncertainty_or_limits: "the 'first and only' claim is unverified; page copy versions rotate; divergence may be copy-lag rather than policy"
  - observation_id: SOBS-021
    source_move_id: M22
    url: https://www.tower28beauty.com/pages/careers-new
    retrieval_date: "2026-07-16"
    short_quote_or_summary: "5 open roles, all marketing/ecommerce/content (Brand Marketing Director + Senior Manager, Ecommerce Director/Senior Manager, Social Media Manager, Director of Content); a Field Sales & Education AE (Central US) surfaced in stale search indexing but not on the live page."
    signal_stage: candidate_support
    claim_it_might_support: current hiring posture concentrated in brand/e-commerce functions (org-motion evidence only, never execution-capacity fact)
    gate_role: org_motion
    independence_hypothesis: official first-party ATS page
    uncertainty_or_limits: listings churn; absence of ops roles on one day is not an org chart
  - observation_id: SOBS-022
    source_move_id: M22
    url: https://www.tower28beauty.com/collections/complexion
    retrieval_date: "2026-07-16"
    short_quote_or_summary: "DTC catalog state: Swipe $24 (21 shades, Bestseller), SunnyDays tint $32 (17 shades, several shades sold out), GetSet powder $28 ('TikTok Viral'), ShineOn Plumping $18 (NEW), LipSoftie $16 (Bestseller), GetSet blush $22 (9 shades), SuperDew $18 (sold out), bundles $50-$88, LipSoftie Deluxe set marked down $128→$118."
    signal_stage: candidate_support
    claim_it_might_support: current DTC price/promotion/availability state incl. shade-level sold-outs and one markdown
    gate_role: none
    independence_hypothesis: official first-party pages
    uncertainty_or_limits: point-in-time; brand labels ('Bestseller', 'TikTok Viral') are self-designations
  - observation_id: SOBS-023
    source_move_id: M23
    url: https://whimsysoul.com/is-tower-28-review/
    retrieval_date: "2026-07-16"
    short_quote_or_summary: "2026-04-16 eczema-reviewer post (verified fetch): 'my skin has genuinely never looked better... I haven't had a rash on my face'; explicit repurchase intent; prefers a Typology concealer over Tower 28's."
    signal_stage: candidate_support
    claim_it_might_support: dated first-person need-state experience with mixed loyalty (SOS praised; concealer substituted)
    gate_role: none
    independence_hypothesis: independent blog; gifting/PR-sample status undisclosed — treat independence as unproven
    uncertainty_or_limits: single reviewer; 91-180-day tier
  - observation_id: SOBS-024
    source_move_id: M24
    url: https://www.youtube.com/watch?v=NfTCoaa3AnQ
    retrieval_date: "2026-07-16"
    short_quote_or_summary: "YouTube comparison genre is dense: vs NARS (~2025-12), vs Saie (~2025-08), Kosas skin-tint comparisons, Hourglass shorts, 'Worth $24 or Overhyped Clean Beauty?' (~2025-10)."
    signal_stage: candidate_support
    claim_it_might_support: the public comparison set around Tower 28 heroes (concealer, skin tint) — value-skepticism framing recurs in titles
    gate_role: none
    independence_hypothesis: unknown — sponsorship/affiliate disclosures unverifiable screen-light (JS pages)
    uncertainty_or_limits: upload dates are search-snippet estimates; titles are not content
  - observation_id: SOBS-025
    source_move_id: M23
    url: https://www.tiktok.com/discover/tower-28-spray-broke-me-out
    retrieval_date: "2026-07-16"
    short_quote_or_summary: "TikTok topic pages indexed under titles 'Tower 28 Spray Broke Me Out', 'Does Tower 28 Spray Cause Purging', 'Tower 28 Concealer Made Me Breakout' (URLs recorded from search indexing only; pages not accessed in-lane)."
    signal_stage: contradiction
    claim_it_might_support: a recurring public breakout/purging complaint theme against the brand's sensitive-skin positioning — theme-level only
    gate_role: none
    independence_hypothesis: unknown; beauty TikTok is heavily gifted/sponsored in both praise and complaint directions
    uncertainty_or_limits: titles are aggregator metadata, not verified content; volume and dates unknown → CR-002
  - observation_id: SOBS-026
    source_move_id: M18
    url: https://www.amazon.sg/s?k=Tower+28+Beauty
    retrieval_date: "2026-07-17"
    short_quote_or_summary: "Amazon International Store (SG vantage) sells Tower 28 (SunnyDays SPF at S$51.94 vs US$32 list; listing shows 905 ratings)."
    signal_stage: candidate_support
    claim_it_might_support: Tower 28 products flow through Amazon international channels at marked-up prices; US amazon.com seller state not observable from this vantage
    gate_role: none
    independence_hypothesis: marketplace page state
    uncertainty_or_limits: geo-redirect prevented US read; official-vs-third-party seller state unknown → CR-003
  - observation_id: SOBS-027
    source_move_id: M20
    url: https://drugstorenews.com/tower-28-announces-pvolve-partnership
    retrieval_date: "2026-07-16"
    short_quote_or_summary: "Trade item framed as February 2026: SOS line placed into Pvolve fitness studios (experiential/wellness channel partnership); the month anchors the article's framing, not an independently verified placement date."
    signal_stage: candidate_support
    claim_it_might_support: dated channel-motion event beyond beauty retail
    gate_role: decision_event
    independence_hypothesis: trade item likely sourced from announcement — one origin
    uncertainty_or_limits: scope/door count and commercial terms not stated; event date is month-level article framing only
  - observation_id: SOBS-028
    source_move_id: M20
    url: https://nationaleczema.org/press-release/tower28scholarshipfund/
    retrieval_date: "2026-07-16"
    short_quote_or_summary: "National Eczema Association press item: Tower 28 scholarship fund; brand claims NEA + rosacea + psoriasis seals across skincare (per SOBS-020)."
    signal_stage: candidate_support
    claim_it_might_support: institutional credibility/partnership facts in the sensitive-skin need-state
    gate_role: none
    independence_hypothesis: NEA is an independent organization with a funding relationship to the brand — partial dependence
    uncertainty_or_limits: press-release class; seal scope verification would need per-product checks
  - observation_id: SOBS-029
    source_move_id: M23
    url: https://brandefyskin.com/blogs/beauty/tower-28-sos-dupe
    retrieval_date: "2026-07-16"
    short_quote_or_summary: "Substitution/price ecosystem: Prequel Universal Skin Solution ($17/4oz) framed against SOS ($28); NYX Bare With Me ($12) against Swipe ($24); SkinSort lists ~50 SOS dupes ('2026')."
    signal_stage: candidate_support
    claim_it_might_support: an organized lower-price substitution narrative around both hero franchises (HOCl spray and concealer)
    gate_role: none
    independence_hypothesis: SEO/affiliate-monetized dupe content — commercial motive, not organic buyer language
    uncertainty_or_limits: dupe-page existence is not switching volume
  - observation_id: SOBS-030
    source_move_id: M21
    url: https://www.tower28beauty.com/blogs/sensitive-content
    retrieval_date: "2026-07-16"
    short_quote_or_summary: "SPF entry: first sunscreen (SOS FaceGuard SPF 30 mineral) reported ~2025-05 (WWD headline, paywalled; dates snippet-level); brand blog 'SPF Shouldn't Be This Hard—So We Fixed It' dated 2025-05-12 corroborates on-site."
    signal_stage: candidate_support
    claim_it_might_support: dated category-entry event (sunscreen/OTC-drug category) within the last ~14 months
    gate_role: decision_event
    independence_hypothesis: announcement-syndicated; brand blog is first-party
    uncertainty_or_limits: exact launch dates unverified by direct primary read (paywall)
```

## Negatives And Access Notes

Negatives (decisive low/no yield, recorded so the report does not re-spend):

- Ulta carriage: no carriage surfaced in the bounded search and brand-list
  checks; the direct Ulta read was bot-blocked, so non-carriage is not proven
  (EQ-015, SOBS-019, M17).
- Search engines return no usable reddit.com links for any Tower 28 query (EQ-010) — the snippet floor for Reddit is currently dead; the sanctioned old.reddit listing route works.
- Quora: login-walled search plus zero index presence (EQ-007, EQ-011) — no lawful anonymous route this pass.
- MakeupAlley: zero search-index yield (EQ-019).
- No funding/acquisition/leadership-change events surfaced 2025-2026 (EQ-016); no NAD/FDA/recall/lawsuit events surfaced (EQ-017).
- Coupon/deal trackers: no intelligence value.
- No dedicated brand press page exists; press contact email only.

Access notes (walls and vantage limits):

- wwd.com → Tollbit paywall (HTTP 402); headlines/snippet dates only, no bypass attempted.
- uspto.report, community.sephora.com, thingtesting.com, skinsort.com → HTTP 403 to fetch tools; community.sephora.com readable via browser (M14, M15).
- reddit thread bodies → login page served to the sanctioned screening route (M12, M13); listings fine.
- ulta.com → bot interstitial in browser (M17).
- amazon.com → geo-redirect to amazon.sg from this vantage (M18).
- revolve.com → search navigation denied in browser (M19); carriage rests on the 2026-07-16 selection-run observation plus the brand stores page.
- TikTok and Instagram → not separately authorized for live reads in this lane; URLs/titles recorded from search indexing only.
- tower28beauty.com → intermittent 503 on parallel fetches; fine sequentially.

## Capture Requests

```yaml
capture_requests:
  - capture_request_id: CR-001
    source_scan: tower28_ci_phase1_2026_07_16
    candidate_or_observation_ids: [SOBS-004, SOBS-005, SOBS-007, SOBS-009, SOBS-011, SOBS-012]
    urls:
      - url: https://old.reddit.com/r/MakeupAddiction/comments/1unb090/tower_28_lipgloss_causing_makeup_separation/
        venue: r/MakeupAddiction
        observation_supported: SOBS-004 failure-mode thread body
        gate_role: none
      - url: https://old.reddit.com/r/MakeupAddiction/comments/1ty47dw/anyone_elses_tower_28_concealer_suck/
        venue: r/MakeupAddiction
        observation_supported: SOBS-005 rejection thread body
        gate_role: none
      - url: https://old.reddit.com/r/Sephora/comments/1tsw0kd/
        venue: r/Sephora
        observation_supported: SOBS-007 mascara rejection/switching body
        gate_role: none
      - url: https://old.reddit.com/r/beauty/comments/1ulo4kf/
        venue: r/beauty
        observation_supported: SOBS-009 brand-evaluation responses
        gate_role: none
      - url: https://old.reddit.com/r/eczema/comments/1sum1co/tower_28_skincare/
        venue: r/eczema
        observation_supported: SOBS-011 need-state discussion body
        gate_role: none
    what_capture_should_verify: thread bodies and response language (praise, complaint, substitution, resolution) behind the dated titles; preserve post dates and visible engagement context as resonance context only
    decision_window: Phase 1 report writing; useful any time before Phase 2 adjudication finalizes
    route_binding_state: unknown
    creator_registry_match_preflight:
      required_when: not_applicable
      receipt_path: null
      intended_action: not_applicable
      decision: not_applicable
      action_status: not_applicable
      can_start_new_capture: not_applicable
    screening_evidence_summary: listings route works and yields dated titles; comment pages serve login walls to the screening route
    uncertainty_or_access_limits: Reddit comment pages may require the browser-rung (CloakBrowser) route Capture owns; no route recommendation made
    not_requested:
      - route_expansion
      - packet_commitment_by_scanning
      - ecr_cleaning_or_judgment_work
  - capture_request_id: CR-002
    source_scan: tower28_ci_phase1_2026_07_16
    candidate_or_observation_ids: [SOBS-025]
    urls:
      - url: https://www.tiktok.com/discover/tower-28-spray-broke-me-out
        venue: TikTok topic page
        observation_supported: SOBS-025 breakout/purging complaint theme
        gate_role: none
      - url: https://www.tiktok.com/discover/tower-28-concealer-made-me-breakout
        venue: TikTok topic page
        observation_supported: SOBS-025 parallel concealer complaint theme
        gate_role: none
    what_capture_should_verify: whether the indexed complaint-theme titles correspond to substantive dated videos, their volume and dates, and campaign/gifting disclosure state; preserve as lawful captures under Capture's own TikTok posture
    decision_window: before Phase 2 treats the breakout/purging theme as more than title-level
    route_binding_state: blocked_outside_current_binding
    creator_registry_match_preflight:
      required_when: not_applicable
      receipt_path: null
      intended_action: not_applicable
      decision: not_applicable
      action_status: not_applicable
      can_start_new_capture: not_applicable
    screening_evidence_summary: TikTok live reads are not authorized in this lane; only search-indexed titles/URLs were recorded
    uncertainty_or_access_limits: complaint themes may be thin or stale behind aggregate topic pages
    not_requested:
      - route_expansion
      - packet_commitment_by_scanning
      - ecr_cleaning_or_judgment_work
  - capture_request_id: CR-003
    source_scan: tower28_ci_phase1_2026_07_16
    candidate_or_observation_ids: [SOBS-019, SOBS-026]
    urls:
      - url: https://www.amazon.com/s?k=Tower+28+Beauty
        venue: Amazon US
        observation_supported: SOBS-026 US seller/storefront state
        gate_role: none
    what_capture_should_verify: from a US vantage — whether an official Tower 28 storefront exists on amazon.com, seller-of-record identity on hero SKUs, price state vs DTC/Sephora, and review volume; resolves the SOBS-019 contradiction (brand stores page omits Amazon while brand-attributed GMV includes it)
    decision_window: before the Phase 1 report makes any channel-control statement about Amazon
    route_binding_state: unknown
    creator_registry_match_preflight:
      required_when: not_applicable
      receipt_path: null
      intended_action: not_applicable
      decision: not_applicable
      action_status: not_applicable
      can_start_new_capture: not_applicable
    screening_evidence_summary: SG geo-vantage saw only the Amazon International Store listing set
    uncertainty_or_access_limits: none beyond vantage
    not_requested:
      - route_expansion
      - packet_commitment_by_scanning
      - ecr_cleaning_or_judgment_work
```

## Candidate Decision

No demand-candidate was minted and none was suppressed: this scan ran under the
`company_competitive_intelligence` commission profile, which is decision-aware
but decision-neutral. Its observations feed the Phase 1 CI report
(`docs/research/forseti_beauty_tower28_company_intelligence_report_v1.md`), not
a demand gate or classifier. No gate was cleared, no Capture route bound, no
demand, pain, buyer, urgency, or GTM conclusion drawn.

## Closeout

```yaml
closeout:
  closeout_state: capture_preservation_only
  csb_rows_fully_executed: [SBR-004, SBR-005, SBR-006, SBR-008, SBR-011, SBR-014, SBR-015, SBR-017, SBR-018, SBR-019, SBR-020]
  csb_rows_partially_executed: [SBR-001, SBR-002, SBR-003, SBR-007, SBR-009, SBR-010]
  csb_rows_not_executable_in_lane: [SBR-012, SBR-013]
  csb_rows_deferred: [SBR-016]
  open_gaps_carried_to_report:
    - subreddit-graph lane output still unsupplied (GAP-001); no mapped Reddit-neighborhood coverage claim
    - Reddit thread bodies unread (CR-001)
    - TikTok/Instagram content unverified beyond indexed titles (CR-002)
    - Amazon US seller state unresolved (CR-003)
    - AEO visibility annotation not run (SBR-016, conditional row)
    - Quora blocked with typed gap
    - per-review text sampling on Sephora PDPs not performed
  boundary_notes: >
    Review counts, ratings, view counts, and engagement context recorded above
    are routing and dispersion context only. They are not demand proof, not
    sell-through, not repeat purchase, not credibility, not gate clearance, and
    not graph weight. Community evidence remains external customer evidence,
    never representative demand or internal company fact.
  next_authorized_step: >
    Seal this scan receipt, run the CSB-first scan checker, then write the
    Phase 1 CI report from these observations and the commission's seed
    observations, applying the Phase 1 gate.
```
