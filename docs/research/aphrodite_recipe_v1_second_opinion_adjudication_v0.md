# Aphrodite Recipe V1 Second Opinion — Adjudication Record v0

```yaml
retrieval_header_version: 1
artifact_role: Research record (cross-vendor second-opinion adjudication — evidence lane, product_learning-capped)
scope: >
  Home-lane adjudication of the OpenAI ChatGPT Pro second opinion on the
  extraction-recipe v1 design for the Aphrodite depth-layer D-1 dress
  rehearsal (commissioned 2026-07-05, package
  aphrodite_recipe_v1_second_opinion_package_v0.zip, SHA256
  65AF9920D7F13694EBA9A2E7D7B5543C152A411FD686EA79E2067B5F615150D2).
  Records the fabrication check, the verdict per section, four
  accept-with-modification rulings, and the bindings recipe v1 must honor.
  The full return is embedded verbatim in the appendix so the receiving
  rehearsal lane can consume the adjudicated material cold.
use_when:
  - Promoting extraction recipe v0 to v1 in the depth-layer rehearsal lane (handoff v1, Work Unit step 2).
  - Checking which second-opinion proposals were accepted, modified, or constrained.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/handoffs/aphrodite_depth_layer_build_handoff_v1.md
  - docs/research/aphrodite_depth_rehearsal_extraction_recipe_v0.md
  - forseti/product/spines/creator_signal/aphrodite_derived_claim_provenance_contract_v0.md
stale_if:
  - Recipe v1 is authored (it then supersedes this record as the operative recipe source).
  - The panel design, provenance contract, or ratified D-1 criteria are amended.
```

## Status

`ADJUDICATED 2026-07-05` — return couriered by the owner from OpenAI ChatGPT
Pro; adversarially reviewed and adjudicated in-lane by the home model (Claude,
this lane). Everything in the appendix remains
`model_asserted_pending_adjudication` EXCEPT as accepted or modified by the
verdicts below. Evidence lane only: not validation, not readiness; adopting
these rulings into recipe v1 is the receiving lane's work under the D-1
handoff.

## Fabrication check (the known cross-vendor failure mode)

Every concrete reference-file fact the return used was verified verbatim
against `fragrance_reference_v0.yaml` before adjudication:

- `product:creed.aventus` exists; note_families `[fruity, sweet, woody,
  leather, citrus]` — exact match (file line 279); tier `niche` — match.
- `product:dior.sauvage` exists; note_families `[fresh, spicy, amber, citrus,
  aromatic, musk, woody]` — exact match (line 260); tier `designer` — match.
- Tier vocabulary `[designer, niche, luxury, creator-owned-dtc, clone-house,
  adjacent]` — exact match (line 96).
- Occasions used (`versatile`, `daily`, `office`) — all in vocabulary
  (line 131); per-product occasions match.
- `dupe_relationships` empty-by-design — correctly carried as honest absence.

**No fabricated facts found.** The synthetic buyer-intake example is usable
as-is.

## Verdicts

| Section of return | Verdict |
| --- | --- |
| Recipe V1 claim-type table (all five panels, 29 claim types) | **ACCEPT**, with modifications M1 and M3 below |
| YouTube adaptations (video atomic unit, segmentation, receipt rule, hashing incl. canonical-packet rule, ad detection, fractional view allocation) | **ACCEPT**, with modifications M2 and M4 below |
| Stance label set (5 labels) and purchase-intent label set (8 labels) | **ACCEPT** as proposed |
| Candidate-set intake schema + synthetic dupe-first example | **ACCEPT** as proposed (fabrication check passed; `intake_source_state` per coordinate is a genuine improvement) |
| Failure forecast (8 failure/mitigation pairs incl. the gate-6 run log) | **ACCEPT** as proposed |

Nothing was rejected outright. Four rulings modify accepted material:

### M1 — Tier facts under the adopted rubric render `show`, not `downgrade`

The return's `fit.tier_alignment` abstention note ("Downgrade if tier facts
are only operator-classified") contradicts the adopted design: tier is BY
DESIGN an operator classification under the in-file rubric
(`vocabulary.tiers.provenance`, adopted 2026-07-05, itself cross-vendor
proposed and in-lane adjudicated). Auto-downgrading every rubric-classified
tier would permanently downgrade the tier row and misrepresent an owner-
adopted decision. **Ruling:** a tier fact whose provenance cites the adopted
rubric renders `show`, with its classification provenance visible per the
claim object; `downgrade` is reserved for facts still marked
`operator_asserted_pending_source` (e.g. occasions, the note_families
vocabulary itself).

### M2 — No blended `liked_support` scalar

The proposed `liked_support = count + sum(like_count)` blends two units into
one number — exactly the composite-score smell the forbidden set exists to
block, in miniature. **Ruling:** display raw comment count and
`sum(like_count)` as two separate numbers (the return's own "shown only
beside raw count" instinct, taken to its conclusion); the top-comment
concentration note is kept.

### M3 — Chip wording is panel-design-owned

`fit.note_family_overlap`'s three chip states ("observed with receipts" /
"observed only via adjacent products" / "withheld — not observed") are
display language. The recipe emits evidence plus the standard
show/downgrade/withhold posture; the panel design record owns the rendered
wording. **Ruling:** accept the three-state evidence distinction; the chip
text maps into the panel design's display vocabulary rather than minting a
parallel display vocabulary inside the recipe.

### M4 — Within-corpus baselines are valid; disclose fractional allocation

(a) The return over-withholds `fit.comparable_brand_baseline` and
`ad.reception_delta` by implying baseline requires cross-cycle history. The
charter's read is within-creator comparison; the 15-video capture window is
itself a valid baseline sample (round-2 precedent). **Ruling:** withhold only
when the corpus itself cannot support a within-window baseline; cross-cycle
baselines remain the S-tier upgrade. (b) Fractional view allocation for
tier/note distributions is accepted as a method choice, but it changes
displayed numbers — **Ruling:** the allocation method is disclosed on-panel
beside the numbers it produces (a method note, not a footnote buried in the
recipe).

## Bindings for recipe v1 (what the receiving lane must honor)

1. The appendix table is the claim-type baseline for all five panels; the
   momentum types' informative-withhold design directly serves ratified D-1
   criterion 3.
2. The YouTube hashing rules (canonical packet per `video_id`, the five-hash
   chain) replace recipe v0's IG corpus hash; the duplicate-packet dedup rule
   is mandatory given the known round-2 clutter.
3. `fit.unresolved_product_mentions` and `intent.sample_limitation` are
   required outputs, not optional — they are the honest-absence surface for
   criterion 2 and the page-1 limitation doctrine respectively.
4. The gate-6 run log (videos read, segments coded, comments coded,
   unresolved count, timestamps, operator steps, exceptions) is the
   bounded-effort receipt; record it during the run, not reconstructed after.
5. Rulings M1–M4 override the corresponding appendix text wherever they
   conflict.

## Non-claims

- Not validation, readiness, buyer proof, or willingness-to-pay evidence;
  `product_learning`-capped.
- Not recipe v1 itself — authoring v1 is the rehearsal lane's Work Unit
  step 2 under the D-1 handoff; not build authorization.
- Does not amend the panel design, the provenance contract, the ratified D-1
  criteria, or the reference file.

## Appendix — the return, verbatim (model_asserted_pending_adjudication except as ruled above)

## Recipe V1 Claim Types
All claim types below should emit the seven derivation-provenance fields plus `provenance_state: show | downgrade | withhold`. A missing required source emits an explicit withhold claim, not a blank row. [Grounding: `aphrodite_derived_claim_provenance_contract_v0.md`, `aphrodite_vetting_sprint_panel_design_v0.md`]

| Panel | Claim type | Definition / rendered element | Level | Evidence source in captured substrate | Expected abstention notes |
|---|---|---|---|---|---|
| Fit | `fit.video_segment_share` | Recent-window share of captured videos that are fragrance-topical and buyer-relevant; classify whole video as review/ranking/clone-guide/haul/other. | corpus | YouTube title, description, transcript cues, per-video metadata. | Withhold if transcript/title/description are unavailable or too thin to classify. [Grounding: `aphrodite_carveout_charter_v0.md`, `aphrodite_depth_rehearsal_round2_gentsscents_grade_v0.md`] |
| Fit | `fit.product_segment_presence` | Product-level mention inventory: resolved product id, video id, segment start/end, deduped product×video mention. Feeds all fit rows. | per-video | Transcript cue spans; title/description only when product is named there; `fragrance_reference_v0.yaml` product ids. | Unresolved mentions emit `fit.unresolved_product_mentions`; they do not roll into tier/note/dupe rows. [Grounding: `fragrance_reference_v0.yaml`, `aphrodite_vetting_sprint_panel_design_v0.md`] |
| Fit | `fit.presence_attention_stance` | Fit-matrix row: videos, deduped product×video mentions, captured views, attention share, stance mix for each product or demand-space. | corpus | `fit.product_segment_presence`, per-video views/likes/comments, stance coding. | Downgrade when attention is one-video dominated; withhold stance if receipts contain mention but no evaluative cue. [Grounding: `aphrodite_vetting_sprint_panel_design_v0.md`, `aphrodite_depth_rehearsal_round2_gentsscents_grade_v0.md`] |
| Fit | `fit.note_family_overlap` | Buyer note-family chips: `observed with receipts`, `observed only via adjacent products`, or `withheld — not observed`. | corpus | Resolved product mentions + `note_families` in `fragrance_reference_v0.yaml` + buyer intake coordinates. | Withhold per family when buyer did not supply it, product resolution fails, or the family exists only as unsupported operator assertion. [Grounding: `fragrance_reference_v0.yaml`, `aphrodite_vetting_sprint_panel_design_v0.md`] |
| Fit | `fit.tier_alignment` | Attention-weighted and editorial coverage distribution across tier vocabulary: designer, niche, luxury, creator-owned-dtc, clone-house, adjacent. | corpus | Resolved products + product/house tier in `fragrance_reference_v0.yaml` + per-video views. | Downgrade if tier facts are only operator-classified; withhold for unresolved products. [Grounding: `fragrance_reference_v0.yaml`, `aphrodite_carveout_charter_v0.md`] — **superseded by ruling M1** |
| Fit | `fit.dupe_direct_original_attention` | Direct-original block for dupe-first buyers: creator attention to each buyer-supplied original target. | corpus | Buyer intake `dupe_target_originals`; transcript product mentions resolved to originals. | Withhold if buyer supplies no original target or target is absent from reference file. [Grounding: `aphrodite_vetting_sprint_panel_design_v0.md`, `fragrance_reference_v0.yaml`] |
| Fit | `fit.dupe_clone_tail_attention` | Clone-tail block: products whose `dupe_of` points to the target original, kept separate from direct original evidence. | corpus | `dupe_of` edges in `fragrance_reference_v0.yaml`; product mentions; views. | Expected withhold in v1 because `dupe_relationships` is empty by design; display honest absence, not zero clone demand. [Grounding: `fragrance_reference_v0.yaml`, `aphrodite_vetting_sprint_panel_design_v0.md`] |
| Fit | `fit.comparable_brand_baseline` | Buyer-comparable content performance versus the creator's own baseline, never versus other creators. | corpus | Buyer intake, resolved comparable brands/products, per-video metrics, creator baseline window. | Withhold when no comparable content or no baseline history exists. [Grounding: `aphrodite_carveout_charter_v0.md`, `aphrodite_vetting_sprint_panel_design_v0.md`] — **modified by ruling M4(a)** |
| Fit | `fit.attention_concentration` | Gameability countermeasure: top-video share, supporting-video count, and whether attention is broadly supported. | corpus | Per-video views and product/demand-space presence. | Downgrade if one viral video carries most attention; never collapse into a score. [Grounding: `aphrodite_vetting_sprint_panel_design_v0.md`] |
| Fit | `fit.niche_share_trajectory` | Time-axis fit read: whether niche/target-space participation is rising or falling across capture cycles. | corpus | Multiple capture cycles; dated product/tier mentions. | Expected withhold for a single capture cycle; name the missing second window. [Grounding: `aphrodite_carveout_charter_v0.md`, `aphrodite_vetting_sprint_panel_design_v0.md`] |
| Fit | `fit.unresolved_product_mentions` | Count and top receipts for product/brand mentions excluded from fit rows due to low-confidence resolution. | corpus | Transcript cue quotes, resolver output, reference lookup failures. | Always show/downgrade when unresolved mentions materially affect denominators; prevents silent drop. [Grounding: `fragrance_reference_v0.yaml`, `aphrodite_vetting_sprint_panel_design_v0.md`] |
| Ad-reception | `ad.video_disclosure_class` | Per-video class: `paid`, `gifted-PR-candidate`, `affiliate-or-self-brand`, `organic`, with confidence and receipt. | per-video | `paidContentOverlay`, description links/disclosure text, title, transcript disclosure cues, creator self-brand markers. | `paidContentOverlay = 0` is not organic proof; affiliate links still classify as affiliate. [Grounding: `aphrodite_depth_rehearsal_round2_gentsscents_grade_v0.md`, `aphrodite_depth_rehearsal_extraction_recipe_v0.md`] |
| Ad-reception | `ad.affiliate_link_inventory` | Per-video affiliate/self-commerce evidence: domains, link counts, discount codes, named storefronts. | per-video | YouTube `short_description`, captured watch metadata. | Withhold only if description metadata is absent; do not infer hidden affiliate use. [Grounding: `aphrodite_depth_rehearsal_round2_gentsscents_grade_v0.md`] |
| Ad-reception | `ad.load_mix` | Corpus density and mix by disclosure class; sponsor/affiliate concentration; disclosure hygiene. | corpus | `ad.video_disclosure_class`, affiliate inventory, platform flag, descriptions. | Downgrade when most videos carry affiliate links and no clean organic comparison set exists. [Grounding: `aphrodite_carveout_charter_v0.md`, `aphrodite_vetting_sprint_panel_design_v0.md`] |
| Ad-reception | `ad.matched_reception_pair` | Sponsored/affiliate/self-commerce video compared to matched organic candidates by topic/date/content type. | per-video | Disclosure class, transcript topic, per-video views/likes/comments, comments. | Withhold if no matched organic candidate exists; do not compare against unrelated viral videos. [Grounding: `aphrodite_vetting_sprint_panel_design_v0.md`] |
| Ad-reception | `ad.reception_delta` | Class-level reception: views/likes/comment texture versus creator's own baseline. | corpus | `ad.matched_reception_pair`, per-video metrics, comment coding. | Downgrade for small n, all-affiliate corpora, or confounded matches. [Grounding: `aphrodite_carveout_charter_v0.md`, `aphrodite_depth_rehearsal_derived_claims_v0.json`] — **modified by ruling M4(a)** |
| Ad-reception | `ad.comment_texture_by_class` | Aggregate comment stance/intent split for commercial vs organic content. | corpus | Engagement-ranked comments with `comment_id`, `like_count`, video id; no usernames. | Withhold if comments are unavailable; display page-1 limitation. [Grounding: `aphrodite_depth_rehearsal_round2_gentsscents_grade_v0.md`, `aphrodite_depth_rehearsal_extraction_recipe_v0.md`] |
| Purchase-intent | `intent.product_resolved_counts` | Product/demand-space intent counts by label: bought-because, where-to-buy, dupe-request, price-objection, comparison-shopping, future-buy. | corpus | Page-1 visible comments, video context, resolved product ids. | Product-level resolution withholds when the comment lacks enough product context; aggregate texture can still show. [Grounding: `aphrodite_vetting_sprint_panel_design_v0.md`, `aphrodite_carveout_charter_v0.md`] |
| Purchase-intent | `intent.engagement_weighted_support` | Same intent labels displayed with raw count and liked-comment support, separately. | corpus | `like_count`, comment rank, comment text. | Downgrade when one high-like comment dominates; never replace raw count with weighted count. [Grounding: `aphrodite_depth_rehearsal_round2_gentsscents_grade_v0.md`] — **modified by ruling M2** |
| Purchase-intent | `intent.aggregate_texture_unresolved` | Intent language that cannot be tied to a product but still indicates audience buying behavior. | corpus | Comments + video-level topic context. | Show as aggregate-only; withhold product/demand-space roll-up. [Grounding: `aphrodite_vetting_sprint_panel_design_v0.md`] |
| Purchase-intent | `intent.sample_limitation` | Visible-comment limitation: page-1/top-sort only, moderation invisible, sample not full audience. | corpus | Comment capture metadata: sampled count, total available comments, sort mode. | Always render as limitation when comment panel is shown. [Grounding: `aphrodite_carveout_charter_v0.md`, `aphrodite_depth_rehearsal_round2_gentsscents_grade_v0.md`] |
| Brand adjacency | `adj.organic_brand_product_presence` | Buyer-like brands/products already discussed unpaid. | per-video / corpus | Product mentions, `ad.video_disclosure_class`, reference tiers/families. | Exclude or downgrade mentions inside paid/affiliate/self-commerce contexts unless organic editorial discussion is separable. [Grounding: `aphrodite_vetting_sprint_panel_design_v0.md`] |
| Brand adjacency | `adj.similarity_to_buyer_coordinates` | Tier/note-family/occasion similarity between organic adjacent products and buyer intake coordinates. | corpus | Buyer intake + `fragrance_reference_v0.yaml`. | Withhold similarity dimensions not supplied by buyer or absent from reference data. [Grounding: `aphrodite_vetting_sprint_panel_design_v0.md`, `fragrance_reference_v0.yaml`] |
| Brand adjacency | `adj.organic_attention_stance` | Attention and stance for adjacent unpaid brands/products. | corpus | Transcript segments, per-video views, stance coding, disclosure classification. | Downgrade if adjacency is present but negative or unclear; presence is not endorsement. [Grounding: `aphrodite_vetting_sprint_panel_design_v0.md`] |
| Brand adjacency | `adj.comparable_brand_baseline` | Organic comparable-brand videos versus creator's own baseline. | corpus | Per-video metrics, organic adjacency set, baseline history. | Withhold with single-window or absent baseline. [Grounding: `aphrodite_carveout_charter_v0.md`, `aphrodite_vetting_sprint_panel_design_v0.md`] — **modified by ruling M4(a)** |
| Momentum | `momentum.capture_window_state` | Whether enough capture cycles exist to show momentum; lists window dates and missing next window. | corpus | Capture timestamps, video publish dates, registry/capture cycle metadata. | Expected show-as-withhold for single-cycle rehearsal. [Grounding: `aphrodite_vetting_sprint_panel_design_v0.md`, `aphrodite_carveout_charter_v0.md`] |
| Momentum | `momentum.view_engagement_moving_average` | Creator-relative moving averages for views/likes/comments over time. | corpus | ≥2 capture cycles with per-video metrics. | Expected withhold on one cycle; do not show raw popularity as momentum. [Grounding: `aphrodite_carveout_charter_v0.md`, `aphrodite_vetting_sprint_panel_design_v0.md`] |
| Momentum | `momentum.follower_delta` | Follower/subscriber count deltas per capture cycle. | corpus | Registry/current-view or captured channel metrics across cycles. | Withhold if registry projection/current-view was not run or only one observation exists. [Grounding: `aphrodite_depth_rehearsal_round2_gentsscents_grade_v0.md`, `aphrodite_carveout_charter_v0.md`] |
| Momentum | `momentum.breakout_frequency` | Frequency of videos outperforming creator's own baseline. | corpus | Historical per-video metrics and capture cycles. | Withhold without baseline; downgrade if baseline window is too short. [Grounding: `aphrodite_carveout_charter_v0.md`] |
| Momentum | `momentum.fit_relevant_participation` | Whether fit-relevant videos are increasing as a share of recent output. | corpus | Product/tier/family mentions across windows. | Expected withhold on one cycle; state what second-cycle comparison would measure. [Grounding: `aphrodite_vetting_sprint_panel_design_v0.md`] |

## YouTube Adaptations

**Input unit rule.** v1 should treat a YouTube video as the atomic source unit, not a Reel shortcode. Each video unit should bind: `video_id`, title, publish date, transcript cue list, watch metadata, `short_description`, `paidContentOverlay`, observed views/likes/comments, and the sampled top-sort comments with `comment_id`, `like_count`, and `reply_count`. [Grounding: `aphrodite_depth_rehearsal_round2_gentsscents_grade_v0.md`, `aphrodite_depth_rehearsal_extraction_recipe_v0.md`]

**Long-transcript segmentation.** For 3,000+ word videos, v1 should emit product-segment claims before whole-video claims. Use explicit chapters if present; otherwise infer segments from product-name spans and transition cues. A whole-video judgment may cite the title/description plus 2–4 segment receipts; it must not cite the entire transcript as the receipt. [Grounding: `aphrodite_depth_rehearsal_round2_gentsscents_grade_v0.md`, `aphrodite_vetting_sprint_panel_design_v0.md`]

**Receipt rule.** Transcript receipts should be verbatim, mechanically greppable, and include `video_id`, `start_ms`, `end_ms`, and the quote. Comment receipts should include `video_id`, `comment_id`, `like_count`, and the verbatim comment text; usernames remain dropped. Aggregate claims should carry a count basis plus top receipts, not paraphrases. [Grounding: `aphrodite_derived_claim_provenance_contract_v0.md`, `aphrodite_depth_rehearsal_extraction_recipe_v0.md`]

**Hashing rule.** Replace v0's IG corpus hash with:
- `transcript_hash = sha256(canonical UTF-8 transcript cue JSON)`
- `watch_metadata_hash = sha256(canonical UTF-8 watch metadata subset used by extraction)`
- `comments_hash = sha256(canonical UTF-8 list of comment_id:text:like_count:reply_count)`
- `video_input_hash = sha256(video_id:transcript_hash:watch_metadata_hash:comments_hash)`
- `corpus_input_hash = sha256("\n".join(video_id:video_input_hash in recipe order))`

For duplicate packets, v1 should name the chosen canonical packet per `video_id` and hash only that packet set. [Grounding: `aphrodite_depth_rehearsal_extraction_recipe_v0.md`, `aphrodite_depth_rehearsal_round2_gentsscents_grade_v0.md`]

**View-weighted attention rule.** Show raw supporting-video count and view-weighted attention separately. For product reach, a video containing the product contributes that video's views once to that product. For tier/note distributions, use fractional allocation: each video's views divided across unique resolved products in that video, so one 25-product list does not overstate every tier. For dupe demand-space reach, count a video once per original demand-space even when multiple products in `D(O)` appear. [Grounding: `aphrodite_vetting_sprint_panel_design_v0.md`, `aphrodite_carveout_charter_v0.md`] — **modified by ruling M4(b): allocation method disclosed on-panel**

**Ad detection rule.** `paidContentOverlay=true` supports paid classification. `paidContentOverlay=false/0` only means no platform paid-promotion overlay was captured; it does not prove organic. Affiliate links, storefront links, discount codes, self-brand commerce, and disclosure phrases in `short_description` should classify the video as `affiliate-or-self-brand` unless stronger paid/gifted evidence is present. [Grounding: `aphrodite_depth_rehearsal_round2_gentsscents_grade_v0.md`, `aphrodite_vetting_sprint_panel_design_v0.md`]

**Comment weighting rule.** Display both raw visible-comment counts and liked-comment support. Suggested operator-light weight: `liked_support = count + sum(like_count)`, shown only beside raw count. Add a top-comment concentration note when one comment supplies most liked support. Do not infer demographics or commenter identity. [Grounding: `aphrodite_depth_rehearsal_round2_gentsscents_grade_v0.md`, `aphrodite_depth_rehearsal_extraction_recipe_v0.md`] — **superseded by ruling M2: no blended scalar; two separate numbers**

**Mention stance label set.**

| Label | Decision rule | Receipt requirement |
| --- | --- | --- |
| `positive_recommend` | Clear praise, recommendation, ranking as good, or stated use-case fit. | Product mention plus evaluative phrase in same cue/segment. |
| `neutral_mention` | Listed, named, or described without clear judgment. | Product mention receipt. |
| `negative_caution` | Clear dislike, warning, poor performance, bad value, or not recommended. | Product mention plus negative evaluative phrase. |
| `mixed_comparative` | Tradeoff or comparison where positive and negative both matter. | Quote showing both sides or comparison target. |
| `unclear` | Sarcasm, ASR ambiguity, unresolved referent, or insufficient context. | Quote plus reason for abstention/downgrade. |

[Grounding: `aphrodite_vetting_sprint_panel_design_v0.md`, `aphrodite_derived_claim_provenance_contract_v0.md`]

**Purchase-intent comment label set.** Use one primary label per comment, with optional secondary only when two intents are explicit.

| Label | Decision rule | Product resolution |
| --- | --- | --- |
| `bought_because_of_creator` | Comment explicitly says purchase/order happened because of this creator/video. | Resolve to product only if named in comment or unambiguous from video segment/title. |
| `where_to_buy` | Asks where/how to buy, stock, link, shipping, or retailer. | Same rule. |
| `dupe_request` | Asks for clone, alternative, "smells like," cheaper version, or dupe comparison. | Resolve to original/demand-space if named; otherwise aggregate dupe texture. |
| `price_objection` | Says product is too expensive or asks for cheaper option. | Product if named; otherwise aggregate. |
| `comparison_shopping` | Asks which of multiple products to choose or compares candidates. | Resolve all named products that exist in reference; unresolved names stay excluded. |
| `future_buy_watchlist` | "On my list," "will buy," "next purchase," without claimed completed purchase. | Product if named or context-supported. |
| `owned_no_creator_causality` | Says they own/bought it, but not because of creator/video. | Do not count as creator-caused conversion; can count as audience ownership texture. |
| `none` | No buying, dupe, price, or shopping intent. | No product-intent claim. |

[Grounding: `aphrodite_vetting_sprint_panel_design_v0.md`, `aphrodite_depth_rehearsal_round2_gentsscents_grade_v0.md`]

## Candidate-Set Intake

Minimal intake schema for the synthetic dupe-first / clone-house lead lane:

| Intake field | Required for rendering | Accepted value shape | Honest-absence handling |
| --- | --- | --- | --- |
| `buyer_segment` | Reading order and dupe-first fit lead. | `dupe_first_clone_house` | If absent, default is not guessed; report uses generic fit order and marks segment-specific rows withheld. |
| `buyer_house_tier` | Tier alignment context. | One tier from `fragrance_reference_v0.yaml`; here `clone-house`. | `value: null`, `posture: withhold`, `reason: buyer tier not supplied`. |
| `dupe_target_originals` | Direct-original and clone-tail demand-space rows. | List of `product:*` ids that exist in `fragrance_reference_v0.yaml`. | Dupe-space rows withhold; do not infer originals from the buyer's brand category. |
| `note_family_targets` | Note-family overlap chips. | List from `vocabulary.note_families`. Can be buyer-supplied or derived from selected originals, but source must be tagged. | Per-family withhold; do not convert empty to "no note preference" unless buyer explicitly says none. |
| `occasion_targets` | Occasion fit chips and product-context framing. | List from `vocabulary.occasions`. | Occasion rows withhold; no lifestyle inference. |
| `target_tier_position` | Whether buyer wants designer-inspired, niche-inspired, luxury-inspired, etc. | List of target original tiers, e.g. `[niche, designer]`. | Tier-position comparison downgrades or withholds if no target tier exists. |
| `intake_source_state` | Provenance for buyer coordinates. | `buyer_supplied`, `derived_from_target_originals`, or `missing_at_intake`. | Required on every coordinate so absence is visible. |

[Grounding: `aphrodite_carveout_charter_v0.md`, `aphrodite_vetting_sprint_panel_design_v0.md`, `fragrance_reference_v0.yaml`]

Concrete filled example using only reference products/families:

```yaml
buyer_profile_id: synthetic_dupe_first_clone_house_v1
buyer_segment: dupe_first_clone_house
buyer_house_tier:
  value: clone-house
  intake_source_state: buyer_supplied
dupe_target_originals:
  - product_id: product:creed.aventus
    name: Aventus
    original_tier: niche
    note_families: [fruity, sweet, woody, leather, citrus]
    occasions: [versatile]
    intake_source_state: buyer_supplied
  - product_id: product:dior.sauvage
    name: Sauvage
    original_tier: designer
    note_families: [fresh, spicy, amber, citrus, aromatic, musk, woody]
    occasions: [versatile, daily]
    intake_source_state: buyer_supplied
note_family_targets:
  required:
    - citrus
    - woody
    - fresh
    - spicy
  acceptable:
    - fruity
    - sweet
    - amber
    - aromatic
  intake_source_state: derived_from_target_originals_plus_buyer_selection
target_tier_position:
  buyer_tier: clone-house
  original_target_tiers: [niche, designer]
  intake_source_state: derived_from_target_originals
occasion_targets:
  values: [versatile, daily, office]
  intake_source_state: buyer_supplied
dupe_graph_state:
  value: no_citable_dupe_edges_in_reference_v0
  rendered_effect: clone_tail_rollup_withheld_direct_original_mentions_still_allowed
```

The key design choice: target originals can render now, but clone-tail roll-up should withhold because `dupe_relationships: []` is the current reference state. [Grounding: `fragrance_reference_v0.yaml`, `aphrodite_vetting_sprint_panel_design_v0.md`]

## Failure Forecast

| Likely failure | Gate risk | Cheapest mitigation inside recipe/panel projection |
| --- | --- | --- |
| Fit rows become operator assertions because the extractor "knows" tiers, notes, or comparable brands without resolving to `fragrance_reference_v0.yaml`. | Gate 2: fit fully derived, no operator-asserted fit facts. | Require every fit claim to list resolved `product_id`, reference field used, and reference provenance. If product or coordinate is absent, emit `withhold`; if field is `operator_asserted_pending_source`, display downgraded provenance state. [Grounding: `aphrodite_carveout_charter_v0.md`, `fragrance_reference_v0.yaml`] |
| Long-form receipts stop being greppable because aggregate claims cite whole videos or paraphrase 3,000-word transcripts. | Gate 3: provenance behavior end-to-end. | Mandate segment receipts with `video_id:start_ms-end_ms` plus verbatim quote; aggregate rows include count basis hash plus top supporting receipts. [Grounding: `aphrodite_derived_claim_provenance_contract_v0.md`, `aphrodite_depth_rehearsal_round2_gentsscents_grade_v0.md`] |
| Momentum over-claims from one capture cycle instead of rendering an informative withhold. | Gate 1 and Gate 3: all five panels rendered; at least one honest withhold displayed. | Momentum panel must emit `momentum.capture_window_state` and withhold moving averages, follower deltas, breakout frequency, and fit-relevant participation until ≥2 cycles exist. [Grounding: `aphrodite_vetting_sprint_panel_design_v0.md`, `aphrodite_carveout_charter_v0.md`] |
| Dupe-first buyer rows look empty because the dupe graph is empty, and the projection accidentally reads that as zero clone demand. | Gate 2 and Gate 4: fit and buyer intake exercised. | Split direct-original and clone-tail rows. Show direct original attention when target originals resolve; show the prescribed honest-absence text for clone tail. [Grounding: `aphrodite_vetting_sprint_panel_design_v0.md`, `fragrance_reference_v0.yaml`] |
| Product resolution fails against a 16-product reference file when long videos name 10–25 products, biasing tier/note/attention rows. | Gate 2: fit resolves against reference coordinates. | Add `fit.unresolved_product_mentions` as a required output: count, top receipts, and excluded-from-rollup reason. Display resolved coverage rate beside tier/note rows. [Grounding: `aphrodite_depth_rehearsal_round2_gentsscents_grade_v0.md`, `fragrance_reference_v0.yaml`] |
| Ad detection treats `paidContentOverlay=0` as organic and misses affiliate-heavy monetization. | Gate 1: ad-reception panel rendered correctly. | Make `paidContentOverlay` only one signal. Description affiliate links, discount codes, and self-commerce create `affiliate-or-self-brand`; organic requires absence of stronger commercial markers. [Grounding: `aphrodite_depth_rehearsal_round2_gentsscents_grade_v0.md`, `aphrodite_vetting_sprint_panel_design_v0.md`] |
| Candidate-set assembly is stubbed rather than exercised with buyer coordinates. | Gate 4: buyer-side product-coordinate intake actually exercised. | Include the synthetic intake object as an input source with its own hash and absence states; fit matrix cannot render segment-specific rows without it. [Grounding: `aphrodite_carveout_charter_v0.md`, `aphrodite_vetting_sprint_panel_design_v0.md`] |
| The hand run becomes heroic and non-repeatable because effort is not recorded. | Gate 6: bounded-effort receipt. | Add a required run log: videos read, transcript segments coded, comments coded, unresolved count, start/end timestamps, operator steps, and exceptions. This is a manual receipt, not new infrastructure. [Grounding: `aphrodite_carveout_charter_v0.md`, `aphrodite_depth_rehearsal_extraction_recipe_v0.md`] |

## Assumptions And Uncertainties

- All proposals here are `model_asserted_pending_adjudication`.
- I assumed recipe v1 may add support claim types as long as it does not change the frozen five-panel display design or six gate criteria. [Grounding: `PROMPT.md`, `aphrodite_carveout_charter_v0.md`, `aphrodite_vetting_sprint_panel_design_v0.md`]
- I assumed the available YouTube substrate for the rehearsal matches the round-2 record: 15 videos, long transcripts, engagement-ranked comments with likes, descriptions with affiliate links, `paidContentOverlay`, and per-video metrics. The raw packets themselves were not included in the ZIP. [Grounding: `aphrodite_depth_rehearsal_round2_gentsscents_grade_v0.md`]
- I assumed `fragrance_reference_v0.yaml` is the only allowed product/house/note/tier/occasion resolution target for the rehearsal, and that its empty `dupe_relationships` list must be rendered as honest absence. [Grounding: `fragrance_reference_v0.yaml`]
- I assumed buyer intake can be represented as a hashed input object for the operator-run session without adding infrastructure. [Grounding: `aphrodite_depth_rehearsal_extraction_recipe_v0.md`, `aphrodite_derived_claim_provenance_contract_v0.md`]
- I treated occasion and some tier fields cautiously because the reference file marks some facts as operator-classified or `operator_asserted_pending_source`; a stricter adjudication may require more downgrade/withhold behavior than the table proposes. [Grounding: `fragrance_reference_v0.yaml`]
- I did not infer any commenter identity, demographic attributes, hidden sponsorship, or legal/brand-safety conclusion; those remain outside the recipe. [Grounding: `aphrodite_carveout_charter_v0.md`, `aphrodite_vetting_sprint_panel_design_v0.md`]
