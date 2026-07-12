# Aphrodite Depth Rehearsal — Extraction Recipe v1 (Report Zero)

```yaml
retrieval_header_version: 1
artifact_role: Research record (versioned rehearsal extraction recipe — computation-lane rehearsal instrument for the D-1 dress rehearsal; not a runner, not display doctrine)
scope: >
  The versioned recipe `aphrodite-rehearsal-extraction-v1` ("Report Zero"
  extraction): the hand-run, model-in-session, NO-API-key recipe that produces
  the D-1 dress rehearsal's derived claims across ALL FIVE Vetting Sprint
  panels (fit, ad-reception, purchase-intent, brand adjacency, momentum) for
  one real captured creator. Promotes recipe v0 per the adjudicated
  cross-vendor second opinion (claim-type baseline, YouTube adaptations,
  stance/purchase-intent label sets, candidate-set intake) with rulings M1–M4
  applied as normative. The DISPLAY rule it satisfies is owned by the Creator
  Signal provenance contract; the panel wording is owned by the panel design
  record; this recipe owns extraction semantics only.
use_when:
  - Hand-running the Report Zero (D-1 dress rehearsal) extraction over the frozen corpus.
  - Reading or re-checking claims that cite extraction_recipe_version aphrodite-rehearsal-extraction-v1.
  - Scoping the later automated depth-layer extractor (this recipe is its hand-run precursor).
authority_boundary: retrieval_only
supersedes:
  - docs/research/aphrodite_depth_rehearsal_extraction_recipe_v0.md   # for rehearsal use; v0 remains the historical record of the round-1/2 hand runs
open_next:
  - docs/research/aphrodite_recipe_v1_second_opinion_adjudication_v0.md   # the adjudicated design this recipe is authored FROM (M1–M4 rulings)
  - forseti/product/spines/creator_signal/aphrodite_derived_claim_provenance_contract_v0.md
  - forseti/product/spines/creator_signal/aphrodite_vetting_sprint_panel_design_v0.md
  - forseti/product/spines/foundation/ontology/fragrance_reference_v0.yaml
stale_if:
  - The derived-claim provenance contract, panel design record, or charter D-1 criteria are amended.
  - A later recipe version supersedes v1.
```

## Recipe identity

- `extraction_recipe_version`: **`aphrodite-rehearsal-extraction-v1`**
- Working name: **Report Zero** — the practice run that produces sprint
  report #0 (the D-1 dress rehearsal) before any paid report #1.
- `extraction_model`: the model executing the hand run records its own exact
  model id in every claim (this run: `claude-fable-5`). Hand-run
  model-in-session under owner dispatch of
  `docs/prompts/handoffs/aphrodite_depth_layer_build_handoff_v1.md`;
  **NO API key, no daemon runner** (owner transport decision 2026-07-05).
  `run_transcript_product_extract.py` is explicitly NOT this recipe's tool.
- Authored FROM: `aphrodite_recipe_v1_second_opinion_adjudication_v0.md`
  (ADJUDICATED 2026-07-05) — the appendix claim-type table and YouTube
  adaptations as accepted there, with **rulings M1–M4 applied as normative**
  wherever they conflict with the appendix text. Full per-claim definitions and
  grounding live in that record; this recipe restates the operative rules and
  the claim-type inventory needed at run time.
- Binds to: `aphrodite_derived_claim_provenance_contract_v0.md` (all seven
  fields; `withhold`, never zero-fill) and the panel design record's display
  rules (panels-never-scores; per-row show/downgrade/withhold).

## Inputs (the frozen corpus, and nothing else)

1. **YouTube video units** (the atomic source unit — v1 replaces v0's IG Reel
   shortcode): per `video_id` — title, publish date, transcript cue list
   (verbatim text + `start_ms`/`end_ms`), watch metadata subset
   (`short_description`, `paidContentOverlay`, observed views/likes/comment
   counts, `taken_at`/publish timestamps), and the sampled top-sort comments
   with `comment_id`, `like_count`, `reply_count`. **Author usernames are
   dropped before extraction** (person-level boundary).
2. **The buyer intake object** (candidate-set assembly input): a hashed YAML
   object per the intake schema below; synthetic unless a waitlist-inbound
   buyer exists at dispatch.
3. **`fragrance_reference_v0.yaml`** — the ONLY product/house/note/tier/
   occasion resolution target. Its empty `dupe_relationships` renders as
   honest absence (panel design §3 empty-graph text), never populated by the
   extractor.

**Canonical-packet rule (mandatory dedup):** where duplicate packets exist for
a `video_id` (the known round-2 clutter: 12 of 15 videos double-captured),
the corpus record names ONE canonical packet set per `video_id` (newest
complete set); hashing and extraction use only that set.

## Hashing rule (the five-hash chain)

- `transcript_hash = sha256(canonical UTF-8 transcript cue JSON)`
- `watch_metadata_hash = sha256(canonical UTF-8 watch-metadata subset used by extraction)`
- `comments_hash = sha256(canonical UTF-8 list of comment_id:text:like_count:reply_count)`
- `video_input_hash = sha256(video_id + ":" + transcript_hash + ":" + watch_metadata_hash + ":" + comments_hash)`
- `corpus_input_hash = sha256("\n".join(video_id + ":" + video_input_hash, in recipe order))`

Per-video claims cite the `video_input_hash`; corpus-level claims cite the
`corpus_input_hash`; buyer-intake-dependent claims additionally cite the
intake object's sha256. Every hash re-derivable from the corpus record alone.

## Receipt rule

- Transcript receipts: verbatim quote + `video_id` + `start_ms`–`end_ms`.
- Comment receipts: verbatim comment text + `video_id` + `comment_id` +
  `like_count`; usernames never appear.
- Grid/watch-metadata receipts: the named field + value (e.g.
  `paidContentOverlay=0`, affiliate domain list).
- Aggregate claims carry a count basis + top supporting receipts — never a
  paraphrase, never "the whole transcript" as receipt.
- Every receipt must be mechanically greppable in its canonical source record.

**Long-transcript segmentation:** for 3,000+ word videos, emit
product-segment claims before whole-video claims (explicit chapters if
present, else product-name spans + transition cues). A whole-video judgment
may cite title/description + 2–4 segment receipts; it must not cite the whole
transcript.

## Derivation-provenance fields (every emitted claim, no exceptions)

Per the provenance contract: `source_refs`, `extraction_model`,
`extraction_recipe_version`, `input_content_hash`, `extraction_timestamp`,
`receipt`, `confidence_or_abstention`, plus
`provenance_state: show | downgrade | withhold`.

## Claim-type inventory (all five panels; definitions per the adjudication appendix)

Fit — `fit.video_segment_share`, `fit.product_segment_presence` (the
per-video product-mention inventory that feeds every fit row),
`fit.presence_attention_stance`, `fit.note_family_overlap`,
`fit.tier_alignment`, `fit.dupe_direct_original_attention`,
`fit.dupe_clone_tail_attention` (expected withhold: empty dupe graph),
`fit.comparable_brand_baseline`, `fit.attention_concentration`,
`fit.niche_share_trajectory` (expected withhold: single cycle),
`fit.unresolved_product_mentions` (**required output**, never optional).

Ad-reception — `ad.video_disclosure_class` (per video: `paid` /
`gifted-PR-candidate` / `affiliate-or-self-brand` / `organic`, each with
confidence + receipt), `ad.affiliate_link_inventory`, `ad.load_mix`,
`ad.matched_reception_pair`, `ad.reception_delta`,
`ad.comment_texture_by_class`.

Purchase-intent — `intent.product_resolved_counts`,
`intent.engagement_weighted_support` (per M2: two separate numbers),
`intent.aggregate_texture_unresolved`, `intent.sample_limitation`
(**required output**: page-1/top-sort-only limitation, always rendered when a
comment panel shows).

Brand adjacency — `adj.organic_brand_product_presence` (paid/affiliate
contexts excluded or downgraded), `adj.similarity_to_buyer_coordinates`,
`adj.organic_attention_stance`, `adj.comparable_brand_baseline`.

Momentum — `momentum.capture_window_state` (**the informative-withhold
carrier**: window dates + the missing next window),
`momentum.view_engagement_moving_average`, `momentum.follower_delta`,
`momentum.breakout_frequency`, `momentum.fit_relevant_participation` — all
expected show-as-withhold on a single capture cycle; single-cycle momentum
must never be shown as a read (drift guard: do not fake momentum to look
complete; the honest withhold satisfies D-1 criterion 3).

## Normative rulings (override the adjudication appendix where they conflict)

- **M1 — tier facts render `show`.** A tier fact whose provenance cites the
  in-file tier rubric (`vocabulary.tiers.provenance`, owner-adopted
  2026-07-05) renders `show` with its classification provenance visible.
  `downgrade` is reserved for reference facts still marked
  `operator_asserted_pending_source` (e.g. occasions, the note_families
  vocabulary itself).
- **M2 — no blended `liked_support` scalar.** Display raw comment count and
  `sum(like_count)` as two separate numbers; keep the top-comment
  concentration note. Never a single blended engagement scalar.
- **M3 — chip wording is panel-design-owned.** The recipe emits the
  three-state evidence distinction (observed-with-receipts /
  observed-only-via-adjacent / not-observed) + show/downgrade/withhold; the
  panel design owns the rendered chip text.
- **M4(a) — within-corpus baselines are valid.** `fit.comparable_brand_baseline`,
  `adj.comparable_brand_baseline`, and `ad.reception_delta` use the capture
  window itself as the within-creator baseline sample; withhold only when the
  corpus cannot support a within-window baseline. Cross-cycle baselines are
  the later S-tier upgrade.
- **M4(b) — fractional view allocation is disclosed on-panel.** Product reach:
  a video containing the product contributes its views once. Tier/note
  distributions: each video's views divided across its unique resolved
  products. Dupe demand-space reach: one video counts once per demand-space.
  The allocation method is displayed beside the numbers it produces.

## Stance label set (mention-level)

| Label | Decision rule | Receipt requirement |
| --- | --- | --- |
| `positive_recommend` | Clear praise, recommendation, ranking as good, or stated use-case fit. | Product mention + evaluative phrase in same cue/segment. |
| `neutral_mention` | Listed, named, or described without clear judgment. | Product mention receipt. |
| `negative_caution` | Clear dislike, warning, poor performance, bad value, not recommended. | Product mention + negative evaluative phrase. |
| `mixed_comparative` | Tradeoff or comparison where positive and negative both matter. | Quote showing both sides or the comparison target. |
| `unclear` | Sarcasm, ASR ambiguity, unresolved referent, insufficient context. | Quote + reason for abstention/downgrade. |

## Purchase-intent label set (one primary per comment; secondary only when two intents are explicit)

| Label | Decision rule | Product resolution |
| --- | --- | --- |
| `bought_because_of_creator` | Explicitly says purchase happened because of this creator/video. | Product only if named in comment or unambiguous from segment/title. |
| `where_to_buy` | Asks where/how to buy, stock, link, shipping, retailer. | Same rule. |
| `dupe_request` | Asks for clone/alternative/"smells like"/cheaper version. | Resolve to original/demand-space if named; else aggregate dupe texture. |
| `price_objection` | Says too expensive or asks cheaper option. | Product if named; else aggregate. |
| `comparison_shopping` | Asks which of multiple products to choose. | Resolve all named products in reference; unresolved stay excluded. |
| `future_buy_watchlist` | "On my list" / "will buy" without claimed completed purchase. | Product if named or context-supported. |
| `owned_no_creator_causality` | Owns/bought it, but not because of creator. | Never a creator-caused conversion; audience-ownership texture only. |
| `none` | No buying/dupe/price/shopping intent. | No product-intent claim. |

## Ad-detection rule

`paidContentOverlay=true` supports `paid`. `paidContentOverlay=false/0` only
means no platform overlay was captured — it does NOT prove organic. Affiliate
links, storefront links, discount codes, self-brand commerce, and disclosure
phrases in `short_description` classify the video `affiliate-or-self-brand`
unless stronger paid/gifted evidence exists. `gifted-PR-candidate` stays a
candidate label (unproven gifting carries its ambiguity in the claim).

## Candidate-set intake schema (criterion 4 input)

Required fields, each carrying `intake_source_state: buyer_supplied |
derived_from_target_originals | missing_at_intake`; absence renders
withhold, never a guess:

`buyer_segment` · `buyer_house_tier` (one reference-file tier) ·
`dupe_target_originals` (list of `product:*` ids existing in the reference) ·
`note_family_targets` (from `vocabulary.note_families`; source tagged) ·
`occasion_targets` (from `vocabulary.occasions`) · `target_tier_position`.

The adjudication's synthetic dupe-first example (Aventus + Sauvage targets,
clone-house buyer; fabrication-checked against the reference file) is the
default intake object when no waitlist-inbound buyer exists at dispatch; the
report states it is synthetic. Clone-tail roll-up withholds
(`dupe_relationships: []` in reference v0) while direct-original mentions
still render — per the panel design's empty-graph rule.

## Abstention rules

- A claim type whose required evidence is absent emits ONE claim object with
  `confidence_or_abstention: "insufficient_evidence"` and
  `provenance_state: withhold`, naming what is missing. Never zero-filled,
  never silently dropped.
- Entity references that do not resolve against the reference file with at
  least medium confidence stay unresolved: they feed
  `fit.unresolved_product_mentions` (count + top receipts + excluded-from-
  rollup reason + resolved-coverage rate displayed beside tier/note rows) and
  never anchor a fit/adjacency claim.
- Every fit claim lists its resolved `product_id`, the reference field used,
  and that field's reference provenance — zero operator-asserted fit facts
  (D-1 criterion 2, mechanically scannable).

## Run log (D-1 criterion 6 — record DURING the run, never reconstructed)

```yaml
report_zero_run_log:
  extraction_recipe_version: aphrodite-rehearsal-extraction-v1
  extraction_model:
  corpus_record:            # path + corpus_input_hash
  buyer_intake_sha256:
  started_at:
  ended_at:
  videos_read:              # count + ids
  transcript_segments_coded:
  comments_coded:
  claims_emitted:           # by panel
  withholds_emitted:        # by claim type
  unresolved_product_mentions:
  operator_steps:           # ordered, honest, including retries
  exceptions_or_surprises:
```

## Forbidden (inherited, restated for the hand run)

No person-level or per-commenter claims; no demographic inference; no vanity
or composite score; no unstamped output; no zero-fill; no blending derived
values with observed metrics (observed counts appear only inside receipts/
inputs, labeled); no claim outside the frozen corpus; no populating the dupe
graph; no momentum read from a single cycle; no API key or daemon runner.

## Non-claims

- Not a runner, extractor build, or capture authorization; a hand-run recipe
  executed model-in-session under the v1 handoff's owner dispatch.
- Not display doctrine (the provenance contract + panel design own display)
  and not a storage schema (rehearsal-grade claim records only; durable store
  is the gated speed-2 pass).
- Not validation or readiness; `product_learning`-capped. Firing D-1 is graded
  against the charter's six criteria by the rehearsal grade record, not
  claimed by this recipe.
