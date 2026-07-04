# Aphrodite Depth Rehearsal — Minimal Fragrance Ontology Slice v0

```yaml
retrieval_header_version: 1
artifact_role: Research record (hand-built rehearsal ontology slice — computation-lane rehearsal artifact, not a promoted ontology)
scope: >
  The minimal fragrance entity slice the jeremyfragrance rehearsal corpus
  needs: houses, products, price tiers, the few note/accord terms observed,
  and scene vocabulary — every entry backed by a receipt from the frozen
  corpus. Built to let the rehearsal's extraction resolve entities; it is NOT
  the fragrance ontology the depth-layer build will create, and its price-tier
  labels are operator-assigned market knowledge, marked as such.
use_when:
  - Resolving entity references in aphrodite_depth_rehearsal derived claims.
  - Sizing what a real fragrance ontology needs beyond a hand slice (see the grade doc).
authority_boundary: retrieval_only
open_next:
  - docs/research/aphrodite_depth_rehearsal_corpus_v0.md
  - docs/research/aphrodite_depth_rehearsal_extraction_recipe_v0.md
stale_if:
  - A real fragrance ontology artifact supersedes rehearsal-slice use.
  - The frozen corpus this slice was built from is superseded.
```

## Build rule

An entity enters this slice only if it appears in the frozen corpus
(`docs/research/aphrodite_depth_rehearsal_corpus_v0.md`), with the receipt
cited. Canonical-name resolution from garbled ASR is marked with a confidence;
entities that cannot be resolved stay in the **unresolved** table rather than
being guessed into the graph. Price-tier labels are operator market knowledge
(not derived from the corpus) and are flagged `operator_assigned`.

Receipts cite `shortcode @ cue start_ms` for transcript cues, `shortcode
caption` for grid captions, and `comment_id` for comments.

## Houses (brands)

| Canonical house | ASR/observed surface form | Tier (operator_assigned) | Receipt | Resolution confidence |
|---|---|---|---|---|
| Dior | "Dior" | designer | DaH3L1Isdrc @ 12620 | high |
| Creed | "Creed" | niche/luxury | DaH3L1Isdrc @ 17060 | high |
| Parfums de Marly | "Parfumse de male" | niche/luxury | DaH3L1Isdrc @ 21260 | medium (ASR-garbled; "Sedley" in same cue is a Parfums de Marly product) |
| Chanel | "Chanel" | designer | DaH3L1Isdrc @ 25220 | high |
| Fragrance One | "My fragrance brand fragrance one" | creator-owned DTC | DaH3L1Isdrc @ 30020; DaKeXcVM0sx caption "www.FRAGRANCE.one" | high |
| Louis Vuitton | "Carolina sorry Louis Vuitton" | luxury designer | DaH3L1Isdrc @ 38020 | high |
| Carolina Herrera | "Carolina Herrera" | designer | DaH3L1Isdrc @ 45000 | high |
| Lancôme | "Lancome" | designer | DaH3L1Isdrc @ 47980 | high |
| Jean Paul Gaultier | "Jean Procté" | designer | DaLBRQiMJhQ @ 3000 | medium-high (garbled house name; "ultra-male" in same cue is a JPG product) |
| Nike Schroeder (Moodsprays) | "Nikos Schroeder" / "Nike Schroeder" / "unsere Moodsprays" | adjacent scent brand (mood sprays) | DaGUhsKsYL9 @ 47130; DaK3uKxBlKy caption; comment 18114708548490508 | medium (host/brand of the Sardinia invite; brand-voiced comment thanks him for liking "our Moodsprays") |

## Products

| Canonical product | House | Observed form | Receipt | Resolution confidence |
|---|---|---|---|---|
| Sauvage | Dior | "Dior Savage" | DaH3L1Isdrc @ 14940 | high (well-known product; ASR homophone) |
| Aventus Absolu | Creed | "Aventus Absolute" | DaH3L1Isdrc @ 18900 | medium-high |
| Sedley | Parfums de Marly | "Sedley" | DaH3L1Isdrc @ 21260 | medium |
| Allure Homme Sport | Chanel | "Allure-Om-Sport" | DaH3L1Isdrc @ 25220 | high |
| Office (For Men) | Fragrance One | "the office fragrance", "OFFICE Fragrance" | DaKd8E9skt8 @ 18000; captions of reels 1,4,5,6,9,10,12 | high |
| The Man | Fragrance One | "the man fragrance" | DaH3L1Isdrc @ 34020 | medium (could be generic phrase; position follows the self-brand cue) |
| Imagination | Louis Vuitton | "imagination" | DaH3L1Isdrc @ 41100 | medium-high |
| Good Girl | Carolina Herrera | "Good girl" | DaH3L1Isdrc @ 46520 | high |
| La Vie Est Belle | Lancôme | "la vie et belle" | DaH3L1Isdrc @ 47980 | high |
| Ultra Male | Jean Paul Gaultier | "ultra-male" | DaLBRQiMJhQ @ 3000 | high |

## Unresolved entity candidates (abstained — NOT in the graph)

| Observed form | Context | Receipt | Why unresolved |
|---|---|---|---|
| "Mekonos … Milk Trox" | introduced as a niche fragrance "that deserves attention … Gorgeous for women" | DaH3L1Isdrc @ 67560–73860 | No confident canonical match from ASR alone; guessing would fabricate an entity |
| "Emerald by Game of Spades" | "Long lasting musky citrus fragrance" | DaH3L1Isdrc @ 80560 | Same: plausible ASR of a niche house+product, no confident resolution |
| "Roasted Sugar" | scent exclamation at the Sardinia resort | DaGUhsKsYL9 @ 44130 | Could be a Moodsprays scent name or loose speech; underdetermined |
| "Unikomotiv" | repeated in German cues around the resort segment | DaGUhsKsYL9 @ 39130, 47130 | ASR artifact, unresolvable |

## Note / accord terms observed

| Term | Receipt |
|---|---|
| "musky citrus" | DaH3L1Isdrc @ 80560 |
| "fresh, long lasting" | DaKd8E9skt8 @ 19000 |

No other note-family vocabulary appears in the corpus. This is the slice's
loudest gap: price-tier and note-family distributions (fit panel component)
cannot be populated from creator speech alone — see the grade doc.

## Dupe relationships

None observed in the corpus (no dupe/clone/alternative discourse in any
transcript, caption, or page-1 comment). Recorded as an explicit absence, not
zero-filled.

## Scene vocabulary

| Term | Meaning in scene | Receipt |
|---|---|---|
| "fragrance of the day" (FOTD) | daily-wear feature slot | DaKd8E9skt8 @ 16000; DaLBhRbskFa @ 3370 |
| "Topseller" | commerce framing of a product | DaIr5aRsp8p caption |
| "final70" | discount code (self-brand commerce) | DaKeXcVM0sx, DaKkwCiB_2B captions |
| "long lasting" | performance/longevity praise axis | DaH3L1Isdrc @ 80560; DaKd8E9skt8 @ 19000 |
| "Prime Jeremy" / "the old Jeremy" | audience era-comparison meme (creator-specific) | comments 18179239690407249, 18159874258478633 |
| "Power" | creator catchphrase referenced by audience | comment 17901243552309541 |

## Non-claims

- Not the fragrance ontology (that is a gated build deliverable); a 10-house
  hand slice covering one creator-week.
- Price tiers are operator-assigned market knowledge, not derived claims, and
  must not be displayed as evidence without independent sourcing.
- Not validation, not readiness, `product_learning`-capped.
