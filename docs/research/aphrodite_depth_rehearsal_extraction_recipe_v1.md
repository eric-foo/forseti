# Aphrodite Depth Rehearsal - Extraction Recipe v1

```yaml
retrieval_header_version: 1
artifact_role: Research record (versioned D-1 rehearsal extraction recipe - operator-run projection, not durable extractor architecture)
scope: >
  Recipe v1 for the Aphrodite D-1 dress rehearsal over one real captured
  YouTube long-form creator. It promotes the v0 hand-run recipe through the
  adjudicated second-opinion rulings, defines the YouTube input/hash/receipt
  rules, and binds all five Vetting Sprint panel claim families to the derived
  claim provenance contract.
use_when:
  - Reading or reviewing the D-1 GentsScents claim record and panel projection.
  - Checking whether the D-1 rehearsal used the adjudicated recipe-v1 rules.
  - Scoping the later durable depth-layer extractor without treating this as storage architecture.
authority_boundary: retrieval_only
open_next:
  - docs/research/aphrodite_recipe_v1_second_opinion_adjudication_v0.md
  - docs/research/aphrodite_depth_rehearsal_d1_gentsscents_corpus_v0.md
  - docs/research/aphrodite_depth_rehearsal_d1_gentsscents_claims_v0.json
  - orca/product/spines/foundation/ontology/fragrance_reference_v0.yaml
stale_if:
  - A later recipe version supersedes this D-1 rehearsal recipe.
  - The derived-claim provenance contract, panel design, or fragrance reference file is amended.
```

## Status

`RECIPE_V1_AUTHORED_FOR_D1_REHEARSAL_PRE_OUTPUT_LIVE_BUNDLE` - evidence lane only,
`product_learning`-capped. This is a hand/operator-run recipe for the D-1
rehearsal artifacts, not a runner, daemon, storage schema, or durable claim
store design. It authorizes no API-key use, no roster-scale capture, no lake
schema, no buyer contact, no FLAG-1 resolution, and no validation/readiness
or buyer-proof claim. Treat the live bundle as pre-output/audit material
unless a later owner gate explicitly promotes it.

## Recipe Identity

- `extraction_recipe_version`: `aphrodite-rehearsal-extraction-v1`
- `extraction_model`: `gpt-5-codex operator-run in-session`
- Transport: operator-runner/model-in-session, no API-key daemon.
- Primary inputs: canonical newest-per-video GentsScents caption packets,
  watch/comment packets, the v1 adjudication record, the panel design, and
  `fragrance_reference_v0.yaml`.
- Claim object contract: every emitted claim carries `source_refs`,
  `extraction_model`, `extraction_recipe_version`, `input_content_hash`,
  `extraction_timestamp`, `receipt`, `confidence_or_abstention`, and
  `provenance_state: show | downgrade | withhold`.

Audit note: `aphrodite_recipe_v1_second_opinion_adjudication_v0.md` describes
the appendix baseline as 29 claim types, but the appendix table enumerates 30
rows when the required `fit.unresolved_product_mentions` output is counted.
This recipe emits every table row and records the count discrepancy rather than
dropping a required honest-absence surface.

## Live Dependency Status

| Dependency | Live status |
| --- | --- |
| D-1 claims JSON | Restored at `docs/research/aphrodite_depth_rehearsal_d1_gentsscents_claims_v0.json`; binds through `extraction_pass.input_content_hash` equal to the corpus hash and `extraction_recipe_version` equal to this recipe version. |
| V1 adjudication record | Restored at `docs/research/aphrodite_recipe_v1_second_opinion_adjudication_v0.md`; retrieval `open_next` repointed to live D-1 files. |
| Derived-claim provenance contract | Verified in `.codex/worktrees/aphrodite-d1-depth-rehearsal/forseti/product/spines/creator_signal/aphrodite_derived_claim_provenance_contract_v0.md`; not restored because live Orca has no accepted `orca/product/spines/creator_signal` destination. |
| Vetting sprint panel design | Verified in `.codex/worktrees/aphrodite-d1-depth-rehearsal/forseti/product/spines/creator_signal/aphrodite_vetting_sprint_panel_design_v0.md`; not restored because live Orca has no accepted `orca/product/spines/creator_signal` destination. |
| Fragrance reference | Restored at `orca/product/spines/foundation/ontology/fragrance_reference_v0.yaml`; this is dated reference data, not validation or fact-truth proof. |

## Input Unit Rule

The atomic input unit is one YouTube video. Each unit binds:

- `video_id`;
- title and publish date;
- caption cue JSON3 packet hash;
- watch/comment packet hash;
- sampled visible comments with per-comment like and reply counts when present;
- description text and link inventory;
- observed view and like counts;
- platform paid-promotion flag when exposed.

Duplicate packets are deduped newest-per-video before hashing. The D-1
GentsScents corpus record names the chosen packet ids and hashes.

## Hashing Rule

Per video:

```text
transcript_hash = sha256(canonical caption packet bytes)
watch_metadata_hash = sha256(canonical watch capture json bytes)
comments_hash = sha256(video-local visible comment text + like_count + reply_count basis)
video_input_hash = sha256(video_id:transcript_hash:watch_metadata_hash:comments_hash)
corpus_input_hash = sha256("\n".join(video_id:video_input_hash in recipe order))
```

The corpus record names the resulting `corpus_input_hash`. The restored D-1
claim file binds to that aggregate through `extraction_pass.input_content_hash`
rather than a separate literal `corpus_input_hash` key. The corpus record stores
per-video input hashes so the aggregate hash is auditable without opening raw
HTML.

## Receipt Rule

Receipts are one of:

- packet id plus file hash and field path for metrics, descriptions, and
  sampled comments;
- `video_id` plus mechanically greppable caption quote for transcript claims;
- reference-coordinate path for fit facts resolved against
  `fragrance_reference_v0.yaml`;
- explicit abstention text naming the missing source for `withhold`.

Aggregate claims carry count basis and top receipts. No aggregate row may cite
"the whole transcript" as its only receipt.

## Claim Types Emitted

Fit panel:

- `fit.video_segment_share`
- `fit.product_segment_presence`
- `fit.presence_attention_stance`
- `fit.note_family_overlap`
- `fit.tier_alignment`
- `fit.dupe_direct_original_attention`
- `fit.dupe_clone_tail_attention`
- `fit.comparable_brand_baseline`
- `fit.attention_concentration`
- `fit.niche_share_trajectory`
- `fit.unresolved_product_mentions`

Ad-reception panel:

- `ad.video_disclosure_class`
- `ad.affiliate_link_inventory`
- `ad.load_mix`
- `ad.matched_reception_pair`
- `ad.reception_delta`
- `ad.comment_texture_by_class`

Purchase-intent panel:

- `intent.product_resolved_counts`
- `intent.engagement_weighted_support`
- `intent.aggregate_texture_unresolved`
- `intent.sample_limitation`

Brand-adjacency panel:

- `adj.organic_brand_product_presence`
- `adj.similarity_to_buyer_coordinates`
- `adj.organic_attention_stance`
- `adj.comparable_brand_baseline`

Momentum panel:

- `momentum.capture_window_state`
- `momentum.view_engagement_moving_average`
- `momentum.follower_delta`
- `momentum.breakout_frequency`
- `momentum.fit_relevant_participation`

## Adjudicated V1 Rulings Applied

- M1: tier facts under the adopted in-file rubric render `show` when the
  tier field resolves to `fragrance_reference_v0.yaml`; they are not
  auto-downgraded merely because the rubric is operator-classified.
- M2: no blended `liked_support` scalar. Raw visible-comment counts and
  `sum(like_count)` render as separate values.
- M3: recipe emits evidence and `show | downgrade | withhold`; panel design
  owns display wording.
- M4: within-corpus baselines are valid for a single-window rehearsal when
  the corpus itself supports them, but fractional allocation methods must be
  disclosed beside the rendered numbers.

## Candidate Intake

This D-1 run exercises a synthetic skeptical dupe-first / clone-house buyer
profile:

```yaml
buyer_profile_id: synthetic_skeptical_dupe_first_clone_house_v1
buyer_segment: dupe_first_clone_house
buyer_house_tier:
  value: clone-house
  intake_source_state: buyer_supplied_synthetic
dupe_target_originals:
  - product:creed.aventus
  - product:dior.sauvage
note_family_targets:
  required: [citrus, woody, fresh, spicy]
  acceptable: [fruity, sweet, amber, aromatic]
  intake_source_state: derived_from_target_originals_plus_skeptical_buyer_selection
occasion_targets:
  values: [versatile, daily, office]
  intake_source_state: buyer_supplied_synthetic
target_tier_position:
  buyer_tier: clone-house
  original_target_tiers: [niche, designer]
```

The profile is synthetic and must be labeled as such on the panel projection.
The skeptical proof posture means weak rows downgrade or withhold rather than
being narrated into a positive recommendation.

## Runbook / Closeout Checklist

1. Start from `docs/research/README.md`, then open this recipe, the D-1 corpus,
   and the D-1 claims JSON without broad repository search.
2. Confirm the claims JSON `extraction_pass.extraction_recipe_version` is
   `aphrodite-rehearsal-extraction-v1` and `extraction_pass.input_content_hash`
   equals the corpus record's `corpus_input_hash`.
3. Treat `input_content_hash` in the claims JSON as the aggregate corpus hash
   binding; do not require or invent a separate `corpus_input_hash` key.
4. Run `Test-Path` for every live Aphrodite `open_next` target from the
   workspace root before claiming the bundle is navigable.
5. Keep remaining non-restored source references as audit limitations, not
   blockers hidden behind positive prose.
6. Preserve non-claims: no validation, readiness, buyer-proof, D-1 passage,
   customer claim schema, build authorization, or durable extractor architecture.

## Forbidden

- No composite, fit score, creator score, or "buy now" answer.
- No unstamped derived claim.
- No zero-filled missingness.
- No person-level or demographic inference from comments.
- No hidden model/API dependency.
- No durable lake lane, claim-store schema, crawler, or roster-scale capture.
- No clone-tail inference without a citable `dupe_of` edge.

## Non-Claims

Recipe v1 is not validation, readiness, buyer proof, willingness-to-pay
evidence, external customer claim schema, or durable extractor architecture.
