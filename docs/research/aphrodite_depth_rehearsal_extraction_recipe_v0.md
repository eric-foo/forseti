# Aphrodite Depth Rehearsal — Extraction Recipe v0

```yaml
retrieval_header_version: 1
artifact_role: Research record (versioned rehearsal extraction recipe — computation-lane rehearsal artifact, not a runner and not display doctrine)
scope: >
  The versioned recipe `aphrodite-rehearsal-extraction-v0` that produced the
  rehearsal's derived claims: inputs, claim types for the fit and ad-reception
  panels, the required derivation-provenance fields, hashing rules, abstention
  rules, and the forbidden set. Capture/computation-lane rehearsal artifact:
  the DISPLAY rule it satisfies is owned by the Creator Signal provenance
  contract; this recipe does not own or amend it.
use_when:
  - Reading or re-running the rehearsal extraction (`aphrodite_depth_rehearsal_derived_claims_v0.json`).
  - Scoping the real depth-layer extractor (this recipe is its hand-run precursor).
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/creator_signal/aphrodite_derived_claim_provenance_contract_v0.md
  - docs/research/aphrodite_depth_rehearsal_corpus_v0.md
stale_if:
  - The derived-claim provenance contract is amended or superseded.
  - A later recipe version supersedes v0 for rehearsal or build use.
```

## Recipe identity

- `extraction_recipe_version`: **`aphrodite-rehearsal-extraction-v0`**
- `extraction_model`: `claude-fable-5` (hand-run by the model in-session; no
  runner exists or is authorized)
- Binds to: `aphrodite_derived_claim_provenance_contract_v0.md` (all seven
  required fields; `withhold`, never zero-fill)
- Existing prior art: the lake's `silver__cleaning__product_mentions` lane
  (`codex-extraction-v0`, rubric 0.4) covers brand/product mentions only; this
  recipe is panel-oriented and additionally covers sponsorship, reception, and
  audience-texture claim types. It reuses nothing from that lane's outputs
  except as a cross-check.

## Inputs (per the frozen corpus, and nothing else)

1. `silver__capture__reel_transcript` records (cue text + timestamps).
2. `silver__capture__audience_comments` records (page-1 comment text,
   comment_id, like_count, created_at; **author usernames are dropped before
   extraction** — person-level boundary).
3. Grid packet metadata rows for the same shortcodes (caption text,
   `is_paid_partnership`, `sponsor_users`, `ad_term_candidates`, like/comment/
   play counts, `taken_at_utc`) from packet `01KWA193403TYNTBJVWAP5W5NE`.

## Claim types

Fit panel (charter Section 4, panel 1):

| Claim type | Definition | Level |
|---|---|---|
| `fit.segment_share` | share of corpus reels whose content is fragrance-topical, judged from transcript+caption together | corpus |
| `fit.product_tier_distribution` | distribution of product mentions across ontology price tiers, with self-brand share separated | corpus |
| `fit.audience_taste_texture` | aggregate page-1 comment texture: supportive vs critical/mocking vs neutral; collector/dupe-seeker discourse presence | corpus (aggregate only) |
| `fit.proven_adjacency` | performance of comparable-brand content vs creator baseline | corpus — expected abstention |
| `fit.niche_share_trajectory` | segment share over time | corpus — expected abstention |

Ad-reception panel (charter Section 4, panel 2):

| Claim type | Definition | Level |
|---|---|---|
| `ad.detection` | per-reel commercial classification: `organic` / `self_brand_commerce` / `gifted_invite_candidate` / `affiliate` / `paid_partnership`, from platform flags + caption/transcript/comment markers, each with confidence + receipt | per reel |
| `ad.load` | density and mix of commercial content; sponsor concentration; disclosure hygiene | corpus |
| `ad.reception` | within-creator engagement comparison between commercial-classified and other reels | corpus |

## Derivation-provenance fields (every emitted claim)

Per the provenance contract, every claim object carries: `source_refs`,
`extraction_model`, `extraction_recipe_version`, `input_content_hash`,
`extraction_timestamp`, `receipt`, `confidence_or_abstention`, plus
`provenance_state: show | downgrade | withhold`.

**Hashing rule.** For a single-reel claim, `input_content_hash` is the sha256
of the exact lake record file(s) the claim was derived from (the same value as
the packet set-record `member_sha256`). For a corpus-level claim,
`input_content_hash` is the sha256 of the UTF-8 string formed by joining, with
`\n`, the ordered list `shortcode:transcript_sha256:comments_sha256` for the
12 corpus rows (order as in the corpus doc). Grid-metadata-derived values cite
the grid packet id + manifest sha256 in `source_refs`. This makes every hash
re-derivable from the corpus doc alone.

**Receipt rule.** Receipts are verbatim quotes (with cue `start_ms` or
`comment_id`) or named grid fields. No paraphrase receipts. A receipt must be
mechanically greppable in its source record.

## Abstention rules

- A claim type whose required evidence is absent emits a single claim object
  with `confidence_or_abstention: "insufficient_evidence"` and
  `provenance_state: withhold`, naming what is missing. Never zero-filled,
  never dropped silently.
- Entity references that cannot be resolved against the ontology slice with at
  least medium confidence stay unresolved (see the slice's unresolved table)
  and cannot anchor a claim.
- `gifted_invite_candidate` is a candidate label by design: an unlabeled hosted
  trip is not proven gifting; the ambiguity is carried in the claim.

## Forbidden (inherited, restated for the hand run)

No person-level or per-commenter claims; no demographic inference; no vanity
score; no unstamped output; no zero-fill; no blending derived values with
observed metrics (grid counts are observed — they appear only inside claim
receipts/inputs, labeled); no claim outside the frozen corpus.

## Non-claims

- Not a runner, extractor build, or capture authorization; a hand-run rehearsal
  recipe executed once by the authoring model.
- Not display doctrine (the provenance contract owns display) and not a
  storage schema.
- Not validation or readiness; `product_learning`-capped.
