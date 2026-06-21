# Beauty Venue Card-Set v0 (promoted trail — the bounded working deck)

```yaml
retrieval_header_version: 1
artifact_role: Promoted venue card-set (the ONE maintained venue asset; bounded by survival ingredients)
scope: >
  The owner-promoted working deck for beauty/personal-care screens (fragrance
  included): 12 cards max, each a dated hint with a review date — which venues (Venue)
  produce, what role each plays in the vertical's signal chain, and the access
  shape that works. Derived entirely from three screens' ledger provenance.
  Read FIRST at Step 0 of any beauty screen, then the provenance grep as usual.
use_when:
  - Step 0 of any authorized beauty/personal-care screen (read before the grep).
  - Reviewing cards at their review dates (owner obligation).
  - Deciding what a future vertical's promoted card-set should look like.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/beauty_venue_card_set_promotion_decision_v0.md   # binding parameters + owner acceptance
  - orca/product/spines/foundation/vertical_exploration/orca_vertical_exploration_guide_v0.md  # the consuming procedure
stale_if:
  - A card passes its review_by date (that card is a stale hint; review or retire it).
  - The promotion decision record is superseded or the set breaches its terms.
```

## Survival Terms (binding; full statement in the promotion record)

Owner: Eric. Hard cap: 12 cards (13th in = one out). Every card:
`review_by 2026-12-11` unless dated otherwise. Cards are dated hints —
fail-soft, try-and-move-on; never current-state claims. Every card cites the
screen ledger(s) it derives from: S1 = batch-1 ledger, S2 = proving screen 2,
S3 = subtle screen 3.

## The Chain (read the cards through this)

- NEWSY class: Reddit boards ORIGINATE -> trade press launders into the
  citable record -> BoF/WWD terminate. Enter via trade hubs (cards 1-3).
- SUBTLE class: nothing launders upward — the detector (WindCaller) IS the record. Enter
  via origination/tracker cards (4-9) and detector cards (10-12).

## Cards (12/12 — cap full)

| # | Venue | Role | What it produced (ledger) | Access shape | review_by |
| --- | --- | --- | --- | --- | --- |
| 1 | Beauty Independent (+ monthly "Indie Beauty Dish" roundups) | producer-hub (newsy) | Richest single screen surface; 5 of 7 S2 candidates traced through it; founder-quote closure/pricing roundups (S1, S2) | direct fetch OK | 2026-12-11 |
| 2 | Glossy | producer (newsy) | Channel-exclusive arcs (Selfless/Target), tariff-pricing coverage incl. cocokind/Saie receipts (S1, S2, S3) | direct fetch OK | 2026-12-11 |
| 3 | BeautyMatter | producer (newsy) | Post-mortems sourcing Reddit timelines (Kinder); byline bridge (Sandler: Glossy->BeautyMatter) (S2, S3) | direct fetch OK | 2026-12-11 |
| 4 | Reddit r/BeautyBoxes | origination / detector-collective | Kinder pre-shutdown decay timeline that trade press adopted as canonical (S2) | direct-HTTP on old.reddit (capture recon PARTIAL->GO, 2026-06-11): `/r/<sub>/search?q=...&restrict_sr=on` (+sort/t) and `/new`, `/top?t=` listings; parse title->/comments/ anchors and row-local submission dates per `docs/workflows/reddit_candidate_intake_old_reddit_search_surface_handling_v0.md`; external search-index discovery unreliable (S3). CAVEAT updated 2026-06-21: WebFetch-based screening agents still cannot fetch reddit.com directly, but the capture lane now exposes orchestrator-invoked `screening_read` for bounded public screening reads (no packet/ECR). First-act old.reddit search receipt closed; `.json` rate ceiling remains a human-rate/backoff note. Walkers record the need; orchestrator routes. | 2026-12-11 |
| 5 | Reddit r/BeautyGuruChatter | origination / detector-collective | Detected Joah's silent wind-down; credited by trade as discovery source (S2) | same read shape as card 4 | 2026-12-11 |
| 6 | Reddit r/AsianBeauty + r/SkincareAddiction | origination | Purito trust-collapse trail; community endorsement power (Stratia calibration) (S1, S2) | same read shape as card 4 | 2026-12-11 |
| 7 | mysubscriptionaddiction.com per-box news pages | tracker | Lifecycle logs with comment-count reaction gauges; 2024-25 signal THIN vs 2020-21 (S1, S2, S3) | direct fetch OK; category pages 404 | 2026-12-11 |
| 8 | Basenotes (megathread 341850 + brand threads + discontinued tags) | tracker — THE fragrance subtle-class home | Routed both S3 fragrance candidates (Puredistance M, Imaginary Authors); detection precedes press by weeks-months (S2, S3) | HTTP 403 direct; search snippets work; archive mementos unreachable via fetch tool this run | 2026-12-11 |
| 9 | Fragrantica (news + designer/product pages) | tracker/aggregator | Discontinued-status confirmations; second aggregation layer for fragrance (S3) | HTTP 403 direct; snippets only | 2026-12-11 |
| 10 | Ingredient-audit blog cluster (toxinfreeclearskin "Ingredient Microscope"; thefiltery) | detector (subtle skincare/haircare) | Detected Evolvh + CLEARSTEM silent reformulations by INCI diff, 1-6mo latency, before any indexed community thread (S3) | direct fetch OK | 2026-12-11 |
| 11 | INCIDecoder | root-receipt detector / wind-caller exemplar (WindCaller) | Commissioned SPF tests = the root receipt the whole Purito chain cites; market-moving detection (S2) | direct fetch OK | 2026-12-11 |
| 12 | Specialist fragrance blog cluster (The Scented Hound, The Plum Girl, CaFleureBon) | outcome gauge (fragrance) | 4 blogs on one ultra-niche SKU change = outsized reception-density; V2Q outcome leg (S3) | direct fetch OK | 2026-12-11 |

## Known Dead / Thin (not cards; don't re-walk without reason)

hellosubscription (thin, categories 404); Change.org petitions (famous-brand
outcomes only in window); Mumsnet/PurseForum discontinuation threads (pre-2019
nostalgia); Deciem Chatroom (excluded-brand adjacency). Full negative sets
live in the three ledgers.

## Non-Claims

Cards are dated hints, not validation or current-state claims. The set
authorizes no screen, no capture, no monitoring; it is consumed only inside an
authorized batch screen via the procedure. Not a general atlas: one vertical,
capped, owned, review-dated. The registry rejection stands for everything else.
