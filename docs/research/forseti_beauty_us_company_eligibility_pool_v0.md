# Forseti Beauty US Company Eligibility Pool v0

```yaml
retrieval_header_version: 1
artifact_role: GTM eligibility and deterministic-selection adjudication
scope: Human-readable adjudication of the 60 eligible US consumer-beauty Brands and the final neutral 20-Brand Phase A pool.
use_when:
  - Explaining which Brands are in the first Beauty company pool and why.
  - Replacing a failed row without changing the accepted selection logic.
  - Auditing the boundary between source evidence and GTM administrative metadata.
authority_boundary: accepted_first_run_research_adjudication
```

## Outcome

The bounded discovery yielded 60 eligible Brands and a deterministic 20-Brand pool. All frozen quotas are filled. No quota was weakened, no Brand was selected for apparent interest, and Scanning made no company-pressure judgment.

The governing rules are in [the Beauty US GTM contract](../../forseti/product/spines/product_lead/gtm/forseti_beauty_us_problem_discovery_to_wedge_contract_v0.md). The complete evidence, hash, skip, and replacement data are in [the machine-readable companion](forseti_beauty_us_company_selection_v0.json). The upstream retrieval receipt is [the neutral longlist scan](forseti_beauty_us_company_longlist_scan_v0.md).

## How selection was performed

Each eligible Brand was normalized, prefixed with `forseti-beauty-us-pool-v0|`, and SHA-256 hashed. In each stratum, the selector reserved the lowest-hash fragrance Brand, then the required lowest-hash comparator rows, then filled remaining slots in ascending hash order. It rejected any later row that would exceed an exact fragrance/comparator quota, the global category cap, or the resolved-parent cap.

Hash values below are shortened for display; the JSON retains all 64 hexadecimal characters.

## Final 20

| evidence row | Brand | stratum | category | fragrance | comparator | resolved parent | hash prefix | deterministic reason |
|---|---|---|---|---|---|---|---|---|
| USBEAUTY-002 | Range Beauty | emerging | makeup | no | no | unresolved | 0c73ce0febf3 | next eligible hash |
| USBEAUTY-003 | BASMA Beauty | emerging | makeup | no | no | unresolved | 509aad793a18 | next eligible hash |
| USBEAUTY-006 | Hyper Skin | emerging | skincare | no | no | unresolved | 2af183743ebc | next eligible hash |
| USBEAUTY-009 | Stratia | emerging | skincare | no | yes | unresolved | 634f7cf166c0 | required comparator |
| USBEAUTY-013 | OUI the People | emerging | body | no | no | unresolved | 34579d9e3c0c | next eligible hash |
| USBEAUTY-016 | Pearfat Parfum | emerging | fragrance | yes | no | unresolved | 3f8727ae19a7 | lowest-hash fragrance |
| USBEAUTY-019 | Tower 28 Beauty | scaling | makeup | no | no | unresolved | 27be278639be | next eligible hash |
| USBEAUTY-021 | ILIA Beauty | scaling | makeup | no | no | Famille C | 40e624cbe759 | next eligible hash |
| USBEAUTY-024 | Rare Beauty | scaling | makeup | no | no | unresolved | 13396bad8be4 | next eligible hash |
| USBEAUTY-027 | Naturium | scaling | skincare | no | no | e.l.f. Beauty | 5210f92bd81f | next eligible hash |
| USBEAUTY-029 | Bubble | scaling | skincare | no | no | unresolved | 6c0bf1f00182 | next eligible hash |
| USBEAUTY-035 | PATTERN Beauty | scaling | haircare | no | no | unresolved | 454e2c76e212 | next eligible hash |
| USBEAUTY-038 | Necessaire | scaling | body | no | no | unresolved | 536189ae2847 | next eligible hash |
| USBEAUTY-039 | Sol de Janeiro | scaling | body | no | no | L'Occitane Groupe | 59a85a961f70 | next eligible hash |
| USBEAUTY-041 | Kopari Beauty | scaling | body | no | yes | unresolved | 6e561c0053cf | required comparator |
| USBEAUTY-045 | Commodity | scaling | fragrance | yes | yes | unresolved | 23b4d50b8cb8 | lowest-hash fragrance; also comparator |
| USBEAUTY-049 | Lancome | established | multi-category | no | no | L'Oreal | 78e39a6bdfc3 | next eligible hash |
| USBEAUTY-052 | Clinique | established | skincare | no | yes | Estee Lauder Companies | 89315fb1fda2 | required comparator |
| USBEAUTY-056 | Bumble and bumble | established | haircare | no | no | Estee Lauder Companies | 840841618d25 | next eligible hash |
| USBEAUTY-059 | DIOR Beauty | established | fragrance | yes | no | LVMH | 684bb683c3ab | lowest-hash fragrance |

## Invariant receipt

| invariant | observed result |
|---|---|
| eligible rows | 60 unique: 18 emerging / 30 scaling / 12 established |
| selected rows | 20 unique: 6 emerging / 10 scaling / 4 established |
| fragrance | 3 exactly: one per stratum |
| low-observed-trigger comparators | 4 exactly: 1 emerging / 2 scaling / 1 established |
| selected categories | makeup 5, skincare 5, body 4, fragrance 3, haircare 2, multi-category 1 |
| non-fragrance category diversity | 5 categories |
| largest resolved-parent group | Estee Lauder Companies: 2 |
| evidence floor | all 60 have two source families, a first-party pointer, a US pointer, public access, and dated observation |
| fragrance replacements | at least two unselected eligible fragrance Brands remain in each stratum |

“Comparator” is administrative sampling metadata. It means the bounded eligibility scan did not surface an obvious pressure trigger. It does not mean the Brand has no acute problem, low pain, weak demand, or low opportunity.

## Evidence trace

For any selected row:

1. Open its `USBEAUTY-###` record in the JSON.
2. Read `identity_state`, `parent_state`, `category`, `channel_types`, and `stratum_evidence`.
3. Verify `source_pointers` contains at least one `brand_owned` first-party pointer and an independently owned `retailer_catalog` pointer.
4. Read `us_market_evidence` and `dated_activity`; `observation_time` proves only that the public surface was visible on 2026-07-16.
5. Read `selection_hash`, `selection_status`, and `selection_reason`. Those are GTM metadata and must not be cited as evidence about the Brand.

## Skips and replacement order

Global replacement rank preserves ascending hash order across all unselected eligible rows. Stratum rank is the usable order for a vacancy in that stratum. A replacement still has to satisfy the exact fragrance/comparator cell and the category/parent caps at replacement time.

| global rank | stratum rank | row | Brand | stratum | skip / violated constraint |
|---:|---:|---|---|---|---|
| 1 | 1 | USBEAUTY-051 | Estee Lauder | established | category cap |
| 2 | 1 | USBEAUTY-010 | RIES | emerging | stratum quota already filled |
| 3 | 2 | USBEAUTY-011 | Sienna Naturals | emerging | comparator quota already filled |
| 4 | 2 | USBEAUTY-050 | NARS | established | category cap |
| 5 | 3 | USBEAUTY-018 | Harlem Perfume Co. | emerging | fragrance quota already filled |
| 6 | 3 | USBEAUTY-060 | Jo Malone London | established | parent cap |
| 7 | 4 | USBEAUTY-004 | Mango People | emerging | category cap |
| 8 | 1 | USBEAUTY-042 | OSEA | scaling | stratum quota already filled |
| 9 | 5 | USBEAUTY-012 | SHAZ & KIKS | emerging | stratum quota already filled |
| 10 | 2 | USBEAUTY-043 | PHLUR | scaling | fragrance quota already filled |
| 11 | 3 | USBEAUTY-028 | BYOMA | scaling | category cap |
| 12 | 4 | USBEAUTY-055 | Benefit Cosmetics | established | category cap |
| 13 | 4 | USBEAUTY-026 | Youth To The People | scaling | category cap |
| 14 | 5 | USBEAUTY-031 | EADEM | scaling | category cap |
| 15 | 6 | USBEAUTY-015 | Hanni | emerging | stratum quota already filled |
| 16 | 6 | USBEAUTY-037 | Ceremonia | scaling | stratum quota already filled |
| 17 | 7 | USBEAUTY-032 | K18 Hair | scaling | stratum quota already filled |
| 18 | 8 | USBEAUTY-044 | The 7 Virtues | scaling | fragrance quota already filled |
| 19 | 9 | USBEAUTY-023 | Glossier | scaling | category cap |
| 20 | 10 | USBEAUTY-020 | Kosas | scaling | category cap |
| 21 | 11 | USBEAUTY-030 | Good Molecules | scaling | category cap |
| 22 | 12 | USBEAUTY-040 | Saltair | scaling | stratum quota already filled |
| 23 | 7 | USBEAUTY-001 | Fara Homidi | emerging | category cap |
| 24 | 5 | USBEAUTY-054 | Kiehl's | established | category cap |
| 25 | 6 | USBEAUTY-057 | Aveda | established | parent cap |
| 26 | 13 | USBEAUTY-033 | Briogeo | scaling | stratum quota already filled |
| 27 | 14 | USBEAUTY-036 | Crown Affair | scaling | comparator quota already filled |
| 28 | 8 | USBEAUTY-017 | Marissa Zappas | emerging | fragrance quota already filled |
| 29 | 7 | USBEAUTY-058 | CHANEL Fragrance and Beauty | established | fragrance quota already filled |
| 30 | 15 | USBEAUTY-048 | Boy Smells | scaling | fragrance quota already filled |
| 31 | 9 | USBEAUTY-014 | 54 Thrones | emerging | comparator quota already filled |
| 32 | 16 | USBEAUTY-025 | Summer Fridays | scaling | category cap |
| 33 | 17 | USBEAUTY-047 | DedCool | scaling | fragrance quota already filled |
| 34 | 8 | USBEAUTY-053 | MAC Cosmetics | established | category cap |
| 35 | 10 | USBEAUTY-005 | Lion Pose | emerging | category cap |
| 36 | 18 | USBEAUTY-022 | Saie | scaling | category cap |
| 37 | 11 | USBEAUTY-007 | Educated Mess | emerging | category cap |
| 38 | 19 | USBEAUTY-034 | amika | scaling | stratum quota already filled |
| 39 | 12 | USBEAUTY-008 | Experiment Beauty | emerging | category cap |
| 40 | 20 | USBEAUTY-046 | Ellis Brooklyn | scaling | fragrance quota already filled |

## Replacement and reopening rule

Replace a selected Brand only when eligibility, identity, lawful access, duplication, or source coverage fails. Begin with the lowest stratum replacement rank that can fill the affected cell and re-evaluate all final-pool constraints. Do not replace a Brand because another looks more interesting.

If no reserve can fill the exact vacancy, fail loudly and reopen Scanning only for that named stratum/category/fragrance/comparator cell. Do not weaken the evidence floor.

## Cold-reader test

Starting only from the GTM contract, a cold reader can reach this artifact, open the JSON, and explain every selected Brand through four distinct facts:

- what public sources established eligibility;
- which observable distribution rule assigned the stratum;
- which hash and quota rule selected the row; and
- which limitations prevent the administrative selection from becoming company evidence.

The route requires no authoring-chat context. It also makes the required stop visible: the first substantive one-company decision-pressure pass remains on hold until the minimal Company Surface-compatible proving slice can preserve facts separately from GTM interpretation.

## Non-claims

This pool is not an ICP, buyer, outreach list, priority ranking, wedge decision, evidence of acute company pain, or Company Surface corpus. It is a neutral, reproducible sampling frame for the next gated research phase.
