# Aphrodite Depth Rehearsal — Extraction Recipe v1

```yaml
retrieval_header_version: 1
artifact_role: Research record (versioned rehearsal extraction recipe — operative computation-lane recipe for the D-1 dress rehearsal; not a runner, not display doctrine)
scope: >
  The versioned recipe `aphrodite-rehearsal-extraction-v1` for the D-1 full
  dress rehearsal: the five-panel claim-type baseline, the seven derivation-
  provenance fields, YouTube hashing/receipt/segmentation rules, the stance and
  purchase-intent label sets, the candidate-set intake schema, the run-log
  (bounded-effort receipt), and the forbidden set. Promotes recipe v0
  (`aphrodite-rehearsal-extraction-v0`, fit + ad-reception only) to all five
  panels per the adjudicated cross-vendor second opinion, with rulings M1-M4
  applied. Operator-run (model-in-session), NO API key.
use_when:
  - Running the D-1 dress-rehearsal extraction over one captured creator's frozen corpus.
  - Scoping the later roster-scale extractor (this recipe is its hand-run precursor).
authority_boundary: retrieval_only
open_next:
  - docs/research/aphrodite_recipe_v1_second_opinion_adjudication_v0.md
  - forseti/product/spines/creator_signal/aphrodite_derived_claim_provenance_contract_v0.md
  - forseti/product/spines/creator_signal/aphrodite_vetting_sprint_panel_design_v0.md
  - forseti/product/spines/foundation/ontology/fragrance_reference_v0.yaml
supersedes:
  - docs/research/aphrodite_depth_rehearsal_extraction_recipe_v0.md
stale_if:
  - The derived-claim provenance contract, the panel design, or the ratified D-1 criteria are amended.
  - A later recipe version supersedes v1.
  - The adjudication's claim-type baseline (its appendix table) is superseded.
```

## Recipe identity

- `extraction_recipe_version`: **`aphrodite-rehearsal-extraction-v1`**
- `extraction_model`: `claude-fable-5` — **hand-run by the model in-session via the
  operator-runner transport; NO API key, no daemon.** `run_transcript_product_extract.py`
  (the key-dependent daemon) is NOT this recipe's tool.
- **Supersedes** `aphrodite-rehearsal-extraction-v0` (fit + ad-reception only, 8 claim types).
- **Authored FROM** `docs/research/aphrodite_recipe_v1_second_opinion_adjudication_v0.md`
  — the adjudicated five-panel / 29-claim design + rulings M1-M4; NOT re-derived from the v0 recipe alone.
- **Binds** `aphrodite_derived_claim_provenance_contract_v0.md`: every claim carries the seven
  required fields + `provenance_state`; `withhold`, never zero-fill.

## What v1 changes vs v0

1. Expands from 2 panels (fit + ad-reception) to **all five panels — 29 claim types**
   (fit, ad-reception, purchase-intent, brand-adjacency, momentum).
2. **YouTube-native**: the video is the atomic source unit (not an IG Reel shortcode);
   long-transcript segmentation; a five-hash chain replaces v0's IG corpus hash.
3. Adds the **stance label set (5)**, the **purchase-intent label set (8)**, and the
   **candidate-set intake schema** (criterion 4).
4. Applies rulings **M1-M4** (below), which override the raw second-opinion return where they conflict.

## Rulings applied (M1-M4 — override the adjudication appendix where they conflict)

- **M1 — tier facts render `show`, not `downgrade`.** A `fit.tier_alignment` fact whose
  provenance cites the adopted in-file tier rubric (`fragrance_reference_v0.yaml`
  `vocabulary.tiers.provenance`) renders `show` with its classification provenance visible.
  `downgrade` is reserved for facts still marked `operator_asserted_pending_source`
  (e.g. occasions, the note-family vocabulary itself). Do NOT auto-downgrade every
  rubric-classified tier.
- **M2 — no blended `liked_support` scalar.** Display raw comment count and
  `sum(like_count)` as **two separate numbers**; keep the top-comment concentration note.
  Never emit a single `count + sum(like_count)` composite (a miniature vanity score).
- **M3 — chip wording is panel-design-owned.** For `fit.note_family_overlap`, the recipe emits
  the three-state evidence distinction (`observed with receipts` / `observed only via adjacent
  products` / `withheld — not observed`) plus the standard show/downgrade/withhold posture;
  the **panel design record owns the rendered chip text.** Do not mint a parallel display vocabulary in the recipe.
- **M4 — within-corpus baselines are valid; disclose fractional allocation.**
  (a) `fit.comparable_brand_baseline`, `ad.reception_delta`, and `adj.comparable_brand_baseline`
  compare against the **creator's own within-window baseline** (the 15-video capture window is a
  valid baseline sample); withhold only when the corpus itself cannot support a within-window
  baseline. Cross-cycle baselines remain the S-tier upgrade.
  (b) Fractional view allocation for tier/note distributions is accepted, but the **allocation
  method is disclosed on-panel** beside the numbers it produces (a method note, not buried in the recipe).

## Inputs (per the frozen corpus; YouTube video as atomic unit)

Freeze the corpus first (an ordered `video_id` list with per-video hashes, so every corpus-level
hash is re-derivable). Each video unit binds: `video_id`, title, publish date, transcript cue list
(`start_ms`/`end_ms` + text), watch metadata, `short_description`, `paidContentOverlay`, observed
views/likes/comments, and the sampled top-sort comments with `comment_id`, `like_count`,
`reply_count`. **Comment author usernames are dropped before extraction** (person-level boundary).
Deduplicate to the canonical newest packet per `video_id` (round-2 clutter: 12/15 videos have duplicate packets).

Resolution target is `fragrance_reference_v0.yaml` and nothing else: houses, products, notes,
accords→family mapping, the in-file tier rubric, `dupe_relationships` (EMPTY by honest absence —
render the panel design's empty-graph text; do not populate it).

## Claim-type baseline (all five panels — 29 types)

The **operative claim-type baseline is the adjudication's appendix table**
(`aphrodite_recipe_v1_second_opinion_adjudication_v0.md`, "Recipe V1 Claim Types"),
with M1-M4 above applied. Every claim emits the seven provenance fields + `provenance_state`.
Index (definitions in the adjudication table):

- **Fit (11):** `fit.video_segment_share`, `fit.product_segment_presence`,
  `fit.presence_attention_stance`, `fit.note_family_overlap` (M3), `fit.tier_alignment` (M1),
  `fit.dupe_direct_original_attention`, `fit.dupe_clone_tail_attention`,
  `fit.comparable_brand_baseline` (M4a), `fit.attention_concentration`,
  `fit.niche_share_trajectory` (expected withhold, single cycle), `fit.unresolved_product_mentions` (required output).
- **Ad-reception (6):** `ad.video_disclosure_class`, `ad.affiliate_link_inventory`, `ad.load_mix`,
  `ad.matched_reception_pair`, `ad.reception_delta` (M4a), `ad.comment_texture_by_class`.
- **Purchase-intent (4):** `intent.product_resolved_counts`, `intent.engagement_weighted_support` (M2),
  `intent.aggregate_texture_unresolved`, `intent.sample_limitation` (required output).
- **Brand-adjacency (4):** `adj.organic_brand_product_presence`, `adj.similarity_to_buyer_coordinates`,
  `adj.organic_attention_stance`, `adj.comparable_brand_baseline` (M4a).
- **Momentum (5):** `momentum.capture_window_state`, `momentum.view_engagement_moving_average`,
  `momentum.follower_delta`, `momentum.breakout_frequency`, `momentum.fit_relevant_participation`.

**Momentum on a single cycle:** `momentum.capture_window_state` shows the window state; the four
longitudinal types emit an informative **withhold** (name the missing second window). This is
correct behavior and satisfies D-1 criterion 3 (honest withhold) — do NOT fake a momentum read to look complete.

**Two required honest-absence outputs (not optional):** `fit.unresolved_product_mentions`
(count + top receipts + excluded-from-rollup reason) and `intent.sample_limitation`
(page-1/top-sort only, moderation invisible, sampled vs total).

## Derivation-provenance fields (every emitted claim)

`source_refs`, `extraction_model`, `extraction_recipe_version`, `input_content_hash`,
`extraction_timestamp`, `receipt`, `confidence_or_abstention`, plus
`provenance_state: show | downgrade | withhold`.

Claim records must be **mechanically scannable** so criterion 2 (zero operator-asserted fit facts)
is provable by grep/script: every fit claim lists its resolved `product_id`, the reference field used,
and the reference provenance; unresolved → `withhold`; `operator_asserted_pending_source` → `downgrade` (per M1).

## Hashing / receipt / segmentation / allocation rules (YouTube)

**Hashing (five-hash chain, replaces v0's IG corpus hash):**
- `transcript_hash = sha256(canonical UTF-8 transcript cue JSON)`
- `watch_metadata_hash = sha256(canonical UTF-8 watch metadata subset used by extraction)`
- `comments_hash = sha256(canonical UTF-8 list of comment_id:text:like_count:reply_count)`
- `video_input_hash = sha256(video_id:transcript_hash:watch_metadata_hash:comments_hash)`
- `corpus_input_hash = sha256("\n".join(video_id:video_input_hash in recipe order))`
- For duplicate packets, name the chosen canonical packet per `video_id` and hash only that packet set.

**Receipt rule.** Verbatim, mechanically greppable. Transcript receipts include `video_id`,
`start_ms`, `end_ms`, and the quote. Comment receipts include `video_id`, `comment_id`,
`like_count`, and the verbatim text; usernames dropped. Aggregate claims carry a count basis
(+ hash) plus top receipts — never paraphrase receipts.

**Segmentation.** For 3,000+ word videos, emit product-segment claims before whole-video claims;
use chapters if present, else infer segments from product-name spans + transition cues. A whole-video
judgment may cite title/description + 2-4 segment receipts; it must NOT cite the entire transcript.

**View-weighted allocation (M4b — disclose on-panel).** Show raw supporting-video count and
view-weighted attention **separately**. Product reach: a video containing the product contributes its
views once to that product. Tier/note distributions: **fractional allocation** — each video's views
divided across the unique resolved products in that video (so a 25-product list doesn't overstate every
tier). Dupe demand-space reach: count a video once per original demand-space. The allocation method is disclosed beside the numbers.

**Ad detection.** `paidContentOverlay=true` supports `paid`. `paidContentOverlay=0` only means no
platform overlay was captured — NOT organic proof. Affiliate/storefront links, discount codes,
self-brand commerce, and disclosure phrases in `short_description` classify the video as
`affiliate-or-self-brand` unless stronger paid/gifted evidence is present.

## Label sets

**Mention stance (one per product mention):** `positive_recommend`, `neutral_mention`,
`negative_caution`, `mixed_comparative`, `unclear` — each with the receipt requirement in the
adjudication table (product mention + evaluative phrase in the same cue/segment; `unclear` carries
its abstention reason).

**Purchase-intent (one primary per comment; optional secondary only when two intents are explicit):**
`bought_because_of_creator`, `where_to_buy`, `dupe_request`, `price_objection`,
`comparison_shopping`, `future_buy_watchlist`, `owned_no_creator_causality`, `none`. Product
resolution per the adjudication rules; unresolved names stay excluded (roll into aggregate texture).

## Abstention rules

- A claim type whose required evidence is absent emits ONE claim object with
  `confidence_or_abstention: "insufficient_evidence"` and `provenance_state: withhold`,
  naming what is missing. Never zero-filled, never dropped silently.
- Entity references not resolvable against the ontology with ≥ medium confidence stay unresolved
  (they surface in `fit.unresolved_product_mentions`) and cannot anchor a claim.
- `dupe_clone_tail_attention` is an **expected withhold** in v1 because `dupe_relationships` is
  empty by design: show the honest-absence text, never zero clone demand. Direct-original attention
  still renders when target originals resolve.
- Missing ≠ zero anywhere; momentum WILL mostly withhold on one cycle (correct).

## Candidate-set intake schema (criterion 4 — exercised, not stubbed)

The buyer-side product-coordinate intake is a hashed input object with per-coordinate
`intake_source_state` (`buyer_supplied` | `derived_from_target_originals` | `missing_at_intake`),
so absence is visible. Required fields: `buyer_segment`, `buyer_house_tier`, `dupe_target_originals`
(product ids that exist in the reference file), `note_family_targets`, `occasion_targets`,
`target_tier_position`, `intake_source_state`. Honest-absence handling per the adjudication's intake
table (defaults are not guessed; unsupplied coordinates withhold their rows). Use the adjudication's
concrete synthetic dupe-first/clone-house example (Aventus/Sauvage) unless a real waitlist-inbound
buyer's coordinates exist at run time; state "synthetic" in the report if synthetic. Record what the
intake needed that did not exist.

## Run-log (bounded-effort receipt — criterion 6)

Record DURING the run, not reconstructed after: videos read, transcript segments coded, comments
coded, unresolved-mention count, start/end timestamps, operator steps, and exceptions. This is a
manual receipt (no new infrastructure); it sizes the later roster-scale build.

## Forbidden (inherited, restated for the hand run)

No person-level or per-commenter claims; no demographic/identity inference; no composite/vanity
score anywhere (a single "should I buy" synthesis is an explicit non-goal); no unstamped output;
no zero-fill; no blending derived values with observed grid metrics (grid counts appear only inside
claim receipts/inputs, labeled); no claim outside the frozen corpus; no dupe-graph population; no
FLAG-1 (commercial-use/data-rights) resolution.

## Non-claims

- Not a runner, extractor build, capture authorization, or roster-scale/lake-schema authorization;
  the hand-run rehearsal recipe executed once by the model in-session.
- Not display doctrine (the panel design + provenance contract own display) and not a storage schema.
- Not validation, readiness, buyer proof, or willingness-to-pay evidence; `product_learning`-capped.
```
